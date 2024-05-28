<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import {
		WEBUI_NAME,
		tags as _tags,
		chatId,
		chats,
		config,
		modelfiles,
		models,
		settings,
		showSidebar,
		user,
		showArchivedChats,
		mobile
	} from '$lib/stores';

	import Tooltip from '$lib/components/common/Tooltip.svelte';

	// import UserMenu from './Sidebar/UserMenu.svelte';
	// import MenuLines from '../icons/MenuLines.svelte';

	import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
	import MenuLines from '$lib/components/icons/MenuLines.svelte';
	import Plyr from '$lib/components/video/Plyr.svelte';

	const i18n = getContext('i18n');

	export let submitPrompt: Function;
	export let stopResponse: Function;

	export let autoScroll = true;
	export let selectedModel = '';

	let chatTextAreaElement: HTMLTextAreaElement;
	let filesInputElement;

	let inputFiles;
	let dragged = false;

	let chatInputPlaceholder = '';

	export let files = [];

	export let fileUploadEnabled = true;
	export let speechRecognitionEnabled = true;

	export let prompt = '';
	export let messages = [];

	let speechRecognition;

	$: if (prompt) {
		if (chatTextAreaElement) {
			chatTextAreaElement.style.height = '';
			chatTextAreaElement.style.height = Math.min(chatTextAreaElement.scrollHeight, 200) + 'px';
		}
	}

	let mediaRecorder;
	let audioChunks = [];
	let isRecording = false;
	const MIN_DECIBELS = -45;

	const scrollToBottom = () => {
		const element = document.getElementById('messages-container');
		element.scrollTop = element.scrollHeight;
	};

	const startRecording = async () => {
		const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
		mediaRecorder = new MediaRecorder(stream);
		mediaRecorder.onstart = () => {
			isRecording = true;
			console.log('Recording started');
		};
		mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
		mediaRecorder.onstop = async () => {
			isRecording = false;
			console.log('Recording stopped');

			// Create a blob from the audio chunks
			const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

			const file = blobToFile(audioBlob, 'recording.wav');

			const res = await transcribeAudio(localStorage.token, file).catch((error) => {
				toast.error(error);
				return null;
			});

			if (res) {
				prompt = res.text;
				await tick();
				chatTextAreaElement?.focus();

				if (prompt !== '' && $settings?.speechAutoSend === true) {
					submitPrompt(prompt, user);
				}
			}

			// saveRecording(audioBlob);
			audioChunks = [];
		};

		// Start recording
		mediaRecorder.start();

		// Monitor silence
		monitorSilence(stream);
	};

	const monitorSilence = (stream) => {
		const audioContext = new AudioContext();
		const audioStreamSource = audioContext.createMediaStreamSource(stream);
		const analyser = audioContext.createAnalyser();
		analyser.minDecibels = MIN_DECIBELS;
		audioStreamSource.connect(analyser);

		const bufferLength = analyser.frequencyBinCount;
		const domainData = new Uint8Array(bufferLength);

		let lastSoundTime = Date.now();

		const detectSound = () => {
			analyser.getByteFrequencyData(domainData);

			if (domainData.some((value) => value > 0)) {
				lastSoundTime = Date.now();
			}

			if (isRecording && Date.now() - lastSoundTime > 3000) {
				mediaRecorder.stop();
				audioContext.close();
				return;
			}

			window.requestAnimationFrame(detectSound);
		};

		window.requestAnimationFrame(detectSound);
	};

	const saveRecording = (blob) => {
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		document.body.appendChild(a);
		a.style = 'display: none';
		a.href = url;
		a.download = 'recording.wav';
		a.click();
		window.URL.revokeObjectURL(url);
	};

	const speechRecognitionHandler = () => {
		// Check if SpeechRecognition is supported

		if (isRecording) {
			if (speechRecognition) {
				speechRecognition.stop();
			}

			if (mediaRecorder) {
				mediaRecorder.stop();
			}
		} else {
			isRecording = true;

			if ($settings?.audio?.STTEngine ?? '' !== '') {
				startRecording();
			} else {
				if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
					// Create a SpeechRecognition object
					speechRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

					// Set continuous to true for continuous recognition
					speechRecognition.continuous = true;

					// Set the timeout for turning off the recognition after inactivity (in milliseconds)
					const inactivityTimeout = 3000; // 3 seconds

					let timeoutId;
					// Start recognition
					speechRecognition.start();

					// Event triggered when speech is recognized
					speechRecognition.onresult = async (event) => {
						// Clear the inactivity timeout
						clearTimeout(timeoutId);

						// Handle recognized speech
						console.log(event);
						const transcript = event.results[Object.keys(event.results).length - 1][0].transcript;

						prompt = `${prompt}${transcript}`;

						await tick();
						chatTextAreaElement?.focus();

						// Restart the inactivity timeout
						timeoutId = setTimeout(() => {
							console.log('Speech recognition turned off due to inactivity.');
							speechRecognition.stop();
						}, inactivityTimeout);
					};

					// Event triggered when recognition is ended
					speechRecognition.onend = function () {
						// Restart recognition after it ends
						console.log('recognition ended');
						isRecording = false;
						if (prompt !== '' && $settings?.speechAutoSend === true) {
							submitPrompt(prompt, user);
						}
					};

					// Event triggered when an error occurs
					speechRecognition.onerror = function (event) {
						console.log(event);
						toast.error($i18n.t(`Speech recognition error: {{error}}`, { error: event.error }));
						isRecording = false;
					};
				} else {
					toast.error($i18n.t('SpeechRecognition API is not supported in this browser.'));
				}
			}
		}
	};

	const uploadDoc = async (file) => {
		console.log(file);

		const doc = {
			type: 'doc',
			name: file.name,
			collection_name: '',
			upload_status: false,
			error: ''
		};

		try {
			files = [...files, doc];

			if (['audio/mpeg', 'audio/wav'].includes(file['type'])) {
				const res = await transcribeAudio(localStorage.token, file).catch((error) => {
					toast.error(error);
					return null;
				});

				if (res) {
					console.log(res);
					const blob = new Blob([res.text], { type: 'text/plain' });
					file = blobToFile(blob, `${file.name}.txt`);
				}
			}

			const res = await uploadDocToVectorDB(localStorage.token, '', file);

			if (res) {
				doc.upload_status = true;
				doc.collection_name = res.collection_name;
				files = files;
			}
		} catch (e) {
			// Remove the failed doc from the files array
			files = files.filter((f) => f.name !== file.name);
			toast.error(e);
		}
	};

	const uploadWeb = async (url) => {
		console.log(url);

		const doc = {
			type: 'doc',
			name: url,
			collection_name: '',
			upload_status: false,
			url: url,
			error: ''
		};

		try {
			files = [...files, doc];
			const res = await uploadWebToVectorDB(localStorage.token, '', url);

			if (res) {
				doc.upload_status = true;
				doc.collection_name = res.collection_name;
				files = files;
			}
		} catch (e) {
			// Remove the failed doc from the files array
			files = files.filter((f) => f.name !== url);
			toast.error(e);
		}
	};

	const uploadYoutubeTranscription = async (url) => {
		console.log(url);

		const doc = {
			type: 'doc',
			name: url,
			collection_name: '',
			upload_status: false,
			url: url,
			error: ''
		};

		try {
			files = [...files, doc];
			const res = await uploadYoutubeTranscriptionToVectorDB(localStorage.token, url);

			if (res) {
				doc.upload_status = true;
				doc.collection_name = res.collection_name;
				files = files;
			}
		} catch (e) {
			// Remove the failed doc from the files array
			files = files.filter((f) => f.name !== url);
			toast.error(e);
		}
	};

	onMount(() => {
		window.setTimeout(() => chatTextAreaElement?.focus(), 0);

		const dropZone = document.querySelector('body');

		const handleKeyDown = (event: KeyboardEvent) => {
			if (event.key === 'Escape') {
				console.log('Escape');
				dragged = false;
			}
		};

		const onDragOver = (e) => {
			e.preventDefault();
			dragged = true;
		};

		const onDragLeave = () => {
			dragged = false;
		};

		const onDrop = async (e) => {
			e.preventDefault();
			console.log(e);

			if (e.dataTransfer?.files) {
				const inputFiles = Array.from(e.dataTransfer?.files);

				if (inputFiles && inputFiles.length > 0) {
					inputFiles.forEach((file) => {
						console.log(file, file.name.split('.').at(-1));
						if (['image/gif', 'image/webp', 'image/jpeg', 'image/png'].includes(file['type'])) {
							let reader = new FileReader();
							reader.onload = (event) => {
								files = [
									...files,
									{
										type: 'image',
										url: `${event.target.result}`
									}
								];
							};
							reader.readAsDataURL(file);
						} else if (
							SUPPORTED_FILE_TYPE.includes(file['type']) ||
							SUPPORTED_FILE_EXTENSIONS.includes(file.name.split('.').at(-1))
						) {
							uploadDoc(file);
						} else {
							toast.error(
								$i18n.t(
									`Unknown File Type '{{file_type}}', but accepting and treating as plain text`,
									{ file_type: file['type'] }
								)
							);
							uploadDoc(file);
						}
					});
				} else {
					toast.error($i18n.t(`File not found.`));
				}
			}

			dragged = false;
		};

		window.addEventListener('keydown', handleKeyDown);

		dropZone?.addEventListener('dragover', onDragOver);
		dropZone?.addEventListener('drop', onDrop);
		dropZone?.addEventListener('dragleave', onDragLeave);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);

			dropZone?.removeEventListener('dragover', onDragOver);
			dropZone?.removeEventListener('drop', onDrop);
			dropZone?.removeEventListener('dragleave', onDragLeave);
		};
	});
</script>

<svelte:head>
	<title>
		{$i18n.t('Video')} | {$WEBUI_NAME}
	</title>
</svelte:head>

<div class="min-h-screen max-h-screen w-full max-w-full flex flex-col">
	<nav id="nav" class=" sticky py-2.5 top-0 flex flex-row justify-center z-30">
		<div class=" flex max-w-full w-full mx-auto px-5 pt-0.5 md:px-[1rem]">
			<div class="flex items-center w-full max-w-full">
				<div
					class="{$showSidebar
						? 'md:hidden'
						: ''} mr-3 self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
				>
					<button
						id="sidebar-toggle-button"
						class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition"
						on:click={() => {
							showSidebar.set(!$showSidebar);
						}}
					>
						<div class=" m-auto self-center">
							<MenuLines />
						</div>
					</button>
				</div>

				<div class="flex justify-between items-center">
					<div class=" text-lg font-semibold self-center">{$i18n.t('Video generation')}</div>
				</div>

				<div
					class="ml-auto self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
				>
					{#if $user !== undefined}
						<UserMenu
							className="max-w-[200px]"
							role={$user.role}
							on:show={(e) => {
								if (e.detail === 'archived-chat') {
									showArchivedChats.set(true);
								}
							}}
						>
							<button
								class="select-none flex rounded-xl p-1.5 w-full hover:bg-gray-100 dark:hover:bg-gray-850 transition"
								aria-label="User Menu"
							>
								<div class=" self-center">
									<img
										src={$user.profile_image_url}
										class="size-6 object-cover rounded-full"
										alt="User profile"
										draggable="false"
									/>
								</div>
							</button>
						</UserMenu>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<div class="video_generation">
		<div class="vieo_generation-enter">
			<form
				dir={$settings?.chatDirection ?? 'LTR'}
				class=" flex flex-col relative w-full rounded-3xl px-1.5 bg-gray-50 dark:bg-gray-850 dark:text-gray-100"
				on:submit|preventDefault={() => {
					submitPrompt(prompt, user);
				}}
			>
				<div class=" flex">
					<textarea
						id="chat-textarea"
						bind:this={chatTextAreaElement}
						class="scrollbar-hidden bg-gray-50 dark:bg-gray-850 dark:text-gray-100 outline-none w-full py-3 px-3 {fileUploadEnabled
							? ''
							: ' pl-4'} rounded-3xl resize-none h-[48px]"
						placeholder={chatInputPlaceholder !== ''
							? chatInputPlaceholder
							: isRecording
							? $i18n.t('Listening...')
							: $i18n.t('Enter video details...')}
						bind:value={prompt}
						on:keypress={(e) => {
							if (
								!$mobile ||
								!(
									'ontouchstart' in window ||
									navigator.maxTouchPoints > 0 ||
									navigator.msMaxTouchPoints > 0
								)
							) {
								if (e.keyCode == 13 && !e.shiftKey) {
									e.preventDefault();
								}
								if (prompt !== '' && e.keyCode == 13 && !e.shiftKey) {
									submitPrompt(prompt, user);
								}
							}
						}}
						on:keydown={async (e) => {
							const isCtrlPressed = e.ctrlKey || e.metaKey; // metaKey is for Cmd key on Mac

							// Check if Ctrl + R is pressed
							if (prompt === '' && isCtrlPressed && e.key.toLowerCase() === 'r') {
								e.preventDefault();
								console.log('regenerate');

								const regenerateButton = [
									...document.getElementsByClassName('regenerate-response-button')
								]?.at(-1);

								regenerateButton?.click();
							}

							if (prompt === '' && e.key == 'ArrowUp') {
								e.preventDefault();

								const userMessageElement = [...document.getElementsByClassName('user-message')]?.at(
									-1
								);

								const editButton = [
									...document.getElementsByClassName('edit-user-message-button')
								]?.at(-1);

								console.log(userMessageElement);

								userMessageElement.scrollIntoView({ block: 'center' });
								editButton?.click();
							}

							if (['/', '#', '@'].includes(prompt.charAt(0)) && e.key === 'ArrowUp') {
								e.preventDefault();

								(promptsElement || documentsElement || modelsElement).selectUp();

								const commandOptionButton = [
									...document.getElementsByClassName('selected-command-option-button')
								]?.at(-1);
								commandOptionButton.scrollIntoView({ block: 'center' });
							}

							if (['/', '#', '@'].includes(prompt.charAt(0)) && e.key === 'ArrowDown') {
								e.preventDefault();

								(promptsElement || documentsElement || modelsElement).selectDown();

								const commandOptionButton = [
									...document.getElementsByClassName('selected-command-option-button')
								]?.at(-1);
								commandOptionButton.scrollIntoView({ block: 'center' });
							}

							if (['/', '#', '@'].includes(prompt.charAt(0)) && e.key === 'Enter') {
								e.preventDefault();

								const commandOptionButton = [
									...document.getElementsByClassName('selected-command-option-button')
								]?.at(-1);

								if (commandOptionButton) {
									commandOptionButton?.click();
								} else {
									document.getElementById('send-message-button')?.click();
								}
							}

							if (['/', '#', '@'].includes(prompt.charAt(0)) && e.key === 'Tab') {
								e.preventDefault();

								const commandOptionButton = [
									...document.getElementsByClassName('selected-command-option-button')
								]?.at(-1);

								commandOptionButton?.click();
							} else if (e.key === 'Tab') {
								const words = findWordIndices(prompt);

								if (words.length > 0) {
									const word = words.at(0);
									const fullPrompt = prompt;

									prompt = prompt.substring(0, word?.endIndex + 1);
									await tick();

									e.target.scrollTop = e.target.scrollHeight;
									prompt = fullPrompt;
									await tick();

									e.preventDefault();
									e.target.setSelectionRange(word?.startIndex, word.endIndex + 1);
								}

								e.target.style.height = '';
								e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
							}

							if (e.key === 'Escape') {
								console.log('Escape');
								selectedModel = '';
							}
						}}
						rows="1"
						on:input={(e) => {
							e.target.style.height = '';
							e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
							// user = null;
						}}
						on:focus={(e) => {
							e.target.style.height = '';
							e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
						}}
						on:paste={(e) => {
							const clipboardData = e.clipboardData || window.clipboardData;

							if (clipboardData && clipboardData.items) {
								for (const item of clipboardData.items) {
									if (item.type.indexOf('image') !== -1) {
										const blob = item.getAsFile();
										const reader = new FileReader();

										reader.onload = function (e) {
											files = [
												...files,
												{
													type: 'image',
													url: `${e.target.result}`
												}
											];
										};

										reader.readAsDataURL(blob);
									}
								}
							}
						}}
					/>

					<div class="self-end mb-2 flex space-x-1 mr-1">
						{#if messages.length == 0 || messages.at(-1).done == true}
							<Tooltip content={$i18n.t('Send message')}>
								<button
									id="send-message-button"
									class="{prompt !== ''
										? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
										: 'text-white bg-gray-200 dark:text-gray-900 dark:bg-gray-700 disabled'} transition rounded-full p-1.5 self-center"
									type="submit"
									disabled={prompt === ''}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 16 16"
										fill="currentColor"
										class="w-5 h-5"
									>
										<path
											fill-rule="evenodd"
											d="M8 14a.75.75 0 0 1-.75-.75V4.56L4.03 7.78a.75.75 0 0 1-1.06-1.06l4.5-4.5a.75.75 0 0 1 1.06 0l4.5 4.5a.75.75 0 0 1-1.06 1.06L8.75 4.56v8.69A.75.75 0 0 1 8 14Z"
											clip-rule="evenodd"
										/>
									</svg>
								</button>
							</Tooltip>
						{:else}
							<button
								class="bg-white hover:bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-800 transition rounded-full p-1.5"
								on:click={stopResponse}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 24 24"
									fill="currentColor"
									class="w-5 h-5"
								>
									<path
										fill-rule="evenodd"
										d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z"
										clip-rule="evenodd"
									/>
								</svg>
							</button>
						{/if}
					</div>
				</div>
			</form>
		</div>
		<div class="vieo_generation-body">
			<div class="vieo_generation-settings">
				<ul class="vieo_generation_results rounded-xl">
					<!-- <li class="vieo_generation_results-item">{$i18n.t('Result 1')}</li>
					<li class="vieo_generation_results-item">{$i18n.t('Result 2')}</li>
					<li class="vieo_generation_results-item">{$i18n.t('Result 3')}</li> -->
				</ul>
				<div class="vieo_generation_params" />
			</div>
			<div class="vieo_generation-preview">
				<Plyr autoplay="true" muted="false" />
				<p class="vieo_generation-description">
					Prompt: <span>A summer Scandinavian forest with tall pines and fir trees, everything is covered with
					moss. High quality, cinematography, 8k, etc. The camera flies low, as if on a throne with
					a good pilot.</span>
				</p>
                <div class="flex justify-end pt-4 text-sm font-medium">
                    <button
                        on:click={() => {
                            localStorage.version = $config.version;
                            show = false;
                        }}
                        class=" px-10 py-3 bg-white hover:bg-white text-black transition rounded-xl"
                    >
                        <span class="relative">{$i18n.t("Download .mp4")}</span>
                    </button>
                </div>
			</div>
		</div>
	</div>
</div>

<style>
	.video_generation {
		display: flex;
		flex-direction: column;
		align-items: center;

		gap: 24px;

		padding: 1.5rem;

		height: calc(100% - 58px);
	}

	.vieo_generation-enter {
		width: 50%;
	}

	.vieo_generation-body {
		display: flex;
		flex-direction: row;
		gap: 16px;

		height: 100%;
		width: 100%;
	}

	.vieo_generation-settings {
		display: flex;
		flex-direction: column;
		gap: 16px;

		height: 100%;
		width: 25%;
	}

	.vieo_generation_results {
		/* display: flex;
		flex-direction: column;
		gap: 12px; */

        background-color: #262626;

        border: 1px dashed white;

		height: 238px;
		width: 100%;
	}

	.vieo_generation_results-item {
		height: 100%;
		width: 100%;

		background-position: center;
		background-repeat: no-repeat;
		background-size: 120%;

		border-radius: 1.5rem;

		color: rgb(255, 255, 255);

		font-size: 16px;
		line-height: 70px;
		font-weight: 600;

		padding: 0 10px;

		transition: all 0.2s ease-in-out;
	}

	.vieo_generation_results-item:hover {
		cursor: pointer;
		background-size: 100%;
	}

	.vieo_generation_results-item:nth-child(1) {
		background-image: url('https://i0.wp.com/picjumbo.com/wp-content/uploads/beautiful-nature-mountain-scenery-with-flowers-free-photo.jpg?w=600&quality=80');
		opacity: 0.35;
	}

	.vieo_generation_results-item:nth-child(2) {
		background-image: url('https://i.natgeofe.com/n/2bd4e99d-63e6-4d10-ba41-957a6d00d5a5/12-forest-bathing-kimelman.jpg');
		opacity: 1;
	}

	.vieo_generation_results-item:nth-child(3) {
		background-image: url('https://img.lovepik.com/photo/48013/0603.jpg_wh860.jpg');
		opacity: 0.35;
	}

	.vieo_generation_params {
		background-color: #262626;
		border-radius: 1.5rem;

		height: calc(100% - 238px);
		width: 100%;
	}

	.vieo_generation-preview {
		width: 75%;
		height: 100%;
	}

	.vieo_generation-description {
		height: 85px;

		margin: 0;

		color: rgb(190, 190, 190);

		font-size: 16px;
		line-height: 24px;
		font-weight: 400;

		padding: 12px 24px;

		background-color: #262626;
		border-radius: 1.5rem;

        display: block;
        margin-top: 14px;
        box-sizing: border-box;
	}

    .vieo_generation-description span{
        color: #ffffff;
    }
</style>
