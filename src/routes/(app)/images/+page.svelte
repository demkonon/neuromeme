<script lang="ts">
	import { writable } from 'svelte/store';
	import { toast } from 'svelte-sonner';
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { onMount, getContext } from 'svelte';
	import { WEBUI_NAME, prompts } from '$lib/stores';
	import { error, text } from '@sveltejs/kit';
	import { goto } from '$app/navigation';
	import ButtonRow from '$lib/components/common/InlineButtons.svelte';

	const i18n = getContext('i18n');

	let chatTextAreaElement: HTMLTextAreaElement;
	let chatInputPlaceholder = '';
	let user = null;

	export let prompt = '';
	export let negativePrompt = '';
	export let submitPrompt: Function;
	export let stopResponse: Function;

	let generatingImage = false;

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { imageGenerations, getImageProgress } from '$lib/apis/images';

	const inputText = writable('');

	let image_url = null;

	const generateImage = async (message) => {
		generatingImage = true;
		image_url = null;

		const res = await imageGenerations(localStorage.token, message, negativePrompt).catch(
			(error) => {
				toast.error(error);
			}
		);

		image_url = res[0].url;

		generatingImage = false;
	};

	function handleGenerateClick(prompt) {
		if (prompt) {
			generateImage(prompt);
			toast.info('Image generation initiated!');
		}
	}

	// Функция для обработки изменений ввода и обновления store
	function handleInputChange(event: Event) {
		const target = event.target as HTMLInputElement;
		inputText.set(target.value);
	}

	let buttons = [
			{
				text: 'Low',
				tooltip: '512x512'
			},
			{
				text: 'Medium',
				tooltip: '728x728'
			},
			{
				text: 'High',
				tooltip: '1024x1024'
			}
		],
		name = 'gallery',
		fit = true;

	const row_btns = {
		buttons,
		name,
		fit
	};

	let buttons_ratio = [
			{
				text: '1:1',
				tooltip: 'Square'
			},
			{
				text: '4:3',
				tooltip: 'Classic'
			},
			{
				text: '16:9',
				tooltip: 'Landscape'
			}
		],
		name_ratio = 'ratio',
		fit_ratio = true;

	const row_btns_ratio = {
		buttons: buttons_ratio,
		name: name_ratio,
		fit: fit_ratio
	};

	let buttons_amount = [
			{
				text: '1',
				tooltip: '1 item'
			},
			{
				text: '2',
				tooltip: '2 items'
			},
			{
				text: '3',
				tooltip: '3 items'
			},
			{
				text: '4',
				tooltip: '4 items'
			}
		],
		name_amount = 'amount',
		fit_amount = true;

	const row_btns_amount = {
		buttons: buttons_amount,
		name: name_amount,
		fit: fit_amount
	};

	let isNegative = false,
		isGallery = true,
		isUpscale = false,
		isFacing = false;
</script>

<svelte:head>
	<title>{$i18n.t('Image Generation')} | {$WEBUI_NAME}</title>
</svelte:head>

<div class="min-h-screen max-h-[100dvh] w-full flex justify-center dark:text-white">
	<div class="flex flex-col justify-between w-full overflow-y-auto p-6">
		<div
			class="mx-auto w-full px-3 md:px-0"
			style="display: flex; flex-direction: row; gap: 20px; height: 100%"
		>
			<div
				style="width: 30%; display: flex; flex-direction: column; align-items: flex-start; overflow: hidden; padding-left: 10px;"
			>
				<form
					class=" flex flex-col relative w-full rounded-3xl px-1.5 border border-gray-100 dark:border-gray-850 bg-white dark:bg-gray-900 dark:text-gray-100"
					on:submit|preventDefault={() => {
						handleGenerateClick(prompt);
					}}
				>
					<div class=" flex" style="width: 100%">
						<textarea
							id="chat-textarea"
							bind:this={chatTextAreaElement}
							class=" dark:bg-gray-900 dark:text-gray-100 outline-none w-full py-3 px-3 rounded-xl resize-none h-[48px]"
							style="border-radius: 14px;"
							placeholder={chatInputPlaceholder !== ''
								? chatInputPlaceholder
								: $i18n.t('Enter prompt')}
							bind:value={prompt}
							on:keypress={(e) => {
								if (e.keyCode == 13 && !e.shiftKey) {
									e.preventDefault();
								}
								if (prompt !== '' && e.keyCode == 13 && !e.shiftKey) {
									submitPrompt(prompt);
								}
							}}
							rows="1"
							on:input={(e) => {
								e.target.style.height = '';
								e.target.style.height = Math.min(e.target.scrollHeight, 100) + 'px';
								user = null;
							}}
							on:focus={(e) => {
								e.target.style.height = '';
								e.target.style.height = Math.min(e.target.scrollHeight, 100) + 'px';
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

						<Tooltip content={$i18n.t('Generate image with stable diffusion')}>
							<button
								class="{prompt !== ''
									? 'bg-black text-white hover:bg-gray-900 dark:bg-white dark:text-black dark:hover:bg-gray-100 '
									: 'text-white bg-gray-100 dark:text-gray-900 dark:bg-gray-800 disabled'} transition rounded-full p-1.5 self-center"
								type="submit"
								disabled={prompt === ''}
								style="padding-left: 24px; padding-right: 24px; display: flex; flex-direction: row; gap: 8px; align-items: center; white-space: nowrap; "
							>
								{$i18n.t('Generate')}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="16"
									height="16"
									fill="currentColor"
									class="w-5 h-5"
									viewBox="0 0 16 16"
								>
									<path
										fill-rule="evenodd"
										d="M9.5 2.672a.5.5 0 1 0 1 0V.843a.5.5 0 0 0-1 0zm4.5.035A.5.5 0 0 0 13.293 2L12 3.293a.5.5 0 1 0 .707.707zM7.293 4A.5.5 0 1 0 8 3.293L6.707 2A.5.5 0 0 0 6 2.707zm-.621 2.5a.5.5 0 1 0 0-1H4.843a.5.5 0 1 0 0 1zm8.485 0a.5.5 0 1 0 0-1h-1.829a.5.5 0 0 0 0 1zM13.293 10A.5.5 0 1 0 14 9.293L12.707 8a.5.5 0 1 0-.707.707zM9.5 11.157a.5.5 0 0 0 1 0V9.328a.5.5 0 0 0-1 0zm1.854-5.097a.5.5 0 0 0 0-.706l-.708-.708a.5.5 0 0 0-.707 0L8.646 5.94a.5.5 0 0 0 0 .707l.708.708a.5.5 0 0 0 .707 0l1.293-1.293Zm-3 3a.5.5 0 0 0 0-.706l-.708-.708a.5.5 0 0 0-.707 0L.646 13.94a.5.5 0 0 0 0 .707l.708.708a.5.5 0 0 0 .707 0z"
										clip-rule="evenodd"
									/>
								</svg>
							</button>
						</Tooltip>
					</div>
				</form>

				<div
					class="negative"
					style="user-select: none; margin-top: 14px; display: flex; flex-direction: row; align-items: center; justify-content: space-between; padding: 0px 12px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Enable negative prompt?')}</p>
					<div class="toggle_element">
						<input type="checkbox" id="switch" bind:checked={isNegative} /><label for="switch"
							>Toggle</label
						>
					</div>
				</div>

				<form
					class="negative-from flex-col relative w-full rounded-3xl px-1.5 border border-gray-100 dark:border-gray-850 bg-white dark:bg-gray-900 dark:text-gray-100"
					class:enable={isNegative}
					on:submit|preventDefault={() => {
						console.log(negativePrompt);
					}}
					style="margin-top: 12px;"
				>
					<div class=" flex" style="width: 100%">
						<textarea
							id="chat-textarea"
							bind:this={chatTextAreaElement}
							class=" dark:bg-gray-900 dark:text-gray-100 outline-none w-full py-3 px-3 rounded-xl resize-none h-[126px]"
							style="border-radius: 14px;"
							placeholder={chatInputPlaceholder !== ''
								? chatInputPlaceholder
								: $i18n.t('Here you can write negative prompt...')}
							bind:value={negativePrompt}
							rows="1"
							on:input={(e) => {
								e.target.style.height = '';
								e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
								user = null;
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
					</div>
				</form>

				<div
					class="quality"
					style="margin-top: 26px; display: flex; flex-direction: column; gap: 8px; padding: 0px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Quality')}</p>
					<ButtonRow {...row_btns} />
				</div>

				<div
					class="quality"
					style="margin-top: 26px; display: flex; flex-direction: column; gap: 8px; padding: 0px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Amount')}</p>
					<ButtonRow {...row_btns_amount} />
				</div>

				<p style="margin-top: 32px;" class="">{$i18n.t('Styles')}</p>

				<div class="radio_list">
					<label for="style_select_real" class="radio_element">
						<div class="radio_example realistic" />
						{$i18n.t('Realistic')}
						<input checked type="radio" name="style_select" id="style_select_real" />
					</label>
					<label for="style_select_anime" class="radio_element">
						<div class="radio_example anime" />
						{$i18n.t('Anime')}
						<input type="radio" name="style_select" id="style_select_anime" />
					</label>
					<label for="style_select_impasto" class="radio_element">
						<div class="radio_example impasto" />
						{$i18n.t('Impasto')}
						<input type="radio" name="style_select" id="style_select_impasto" />
					</label>
					<label for="style_select_scifi" class="radio_element">
						<div class="radio_example scifi" />
						{$i18n.t('Sci fi')}
						<input type="radio" name="style_select" id="style_select_scifi" />
					</label>
				</div>

				<div
					class="negative"
					style="user-select: none; margin-top: 26px; display: flex; flex-direction: row; align-items: center; justify-content: space-between; padding: 0px 12px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Save in gallery')}</p>
					<div class="toggle_element">
						<input type="checkbox" id="switch" bind:checked={isGallery} /><label for="switch"
							>Toggle</label
						>
					</div>
				</div>

				<!-- <div
					class="ration"
					style="margin-top: 14px; display: flex; flex-direction: column; gap: 16px; padding: 0px 10px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Aspect ratio')}</p>
					<div
						class="ration_list"
						style="display: flex; flex-direction: row;"
					>
						<label class="ration_element 4_3" for="ratio_select_1">
							<div class="ratio_image"></div>
							4:3
							<input type="radio" name="ratio_select" id="ratio_select_1">
						</label>
						<label class="ration_element 1_1" for="ratio_select_2">
							<div class="ratio_image"></div>
							1:1
							<input type="radio" name="ratio_select" id="ratio_select_2">
						</label>
						<label class="ration_element 16_9" for="ratio_select_3">
							<div class="ratio_image"></div>
							16:9
							<input type="radio" name="ratio_select" id="ratio_select_3">
						</label>
					</div>
				</div> -->

				<div
					class="Ratio"
					style="margin-top: 42px; display: flex; flex-direction: column; gap: 8px; padding: 0px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Ratio')}</p>
					<ButtonRow {...row_btns_ratio} />
				</div>

				<div
					class="negative"
					style="user-select: none; margin-top: 18px; display: flex; flex-direction: row; align-items: center; justify-content: space-between; padding: 0px 12px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Upscale 2x')}</p>
					<div class="toggle_element">
						<input type="checkbox" id="switch" bind:checked={isUpscale} /><label for="switch"
							>Toggle</label
						>
					</div>
				</div>

				<div
					class="negative"
					style="user-select: none; margin-top: 18px; display: flex; flex-direction: row; align-items: center; justify-content: space-between; padding: 0px 12px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Better faces (GFPGAN)')}</p>
					<div class="toggle_element">
						<input type="checkbox" id="switch" bind:checked={isFacing} /><label for="switch"
							>Toggle</label
						>
					</div>
				</div>

				<!-- <div
					class="negative"
					style="margin-top: 26px; display: flex; flex-direction: column; gap: 16px; padding: 0px 10px; box-sizing: border-box; width: 100%;"
				>
					<p class="">{$i18n.t('Primary colors')}</p>
					<div
						class="palette_container"
						style="display: flex; flex-direction: row; flex-wrap: wrap;"
					>
						<input type="radio" name="color" id="red" value="red" />
						<label for="red"><span class="red" /></label>

						<input type="radio" name="color" id="green" />
						<label for="green"><span class="green" /></label>

						<input type="radio" name="color" id="yellow" />
						<label for="yellow"><span class="yellow" /></label>

						<input type="radio" name="color" id="olive" />
						<label for="olive"><span class="olive" /></label>

						<input type="radio" name="color" id="orange" />
						<label for="orange"><span class="orange" /></label>

						<input type="radio" name="color" id="teal" />
						<label for="teal"><span class="teal" /></label>

					</div>
				</div>
				<label for="select_ref" class="drop-zone">
					<div class="drop-zone_image"></div>
					<p class="drop-zone_text"><span>Upload or drag and drop</span> an image <br/> to use as input</p>
					<input id="select_ref" type="file" style="display: none;"/>
				</label> -->
			</div>
			<div
				class="placeholder_generated"
				style="overflow: hidden;"
				class:animation={generatingImage === true}
			>
				{#if image_url}
					<ul class="control_panel">
						<li
							class="control_element save"
							on:click={() => {
								if(image_url){
									fetch(image_url)
									.then((response) => response.blob()) // Получаем данные в виде блоба
									.then((blob) => {
										// Создаем ссылку на скачивание фото
										const link = document.createElement('a');
										link.href = URL.createObjectURL(blob);
										link.download = 'generation_neuro_image.jpg'; // Задаем имя файла для скачивания
										// Имитируем клик на ссылку для начала загрузки файла
										link.click();
									})
									.catch((error) => console.error('Error while downloading image:', error));
								}
							}}
						/>
						<li
							class="control_element retry"
							on:click={() => {
								if (prompt) {
									handleGenerateClick(prompt);
								}
							}}
						/>
						<!-- <li class="control_element settings"></li> -->
						<li class="control_element delete" />
						<!-- <li class="control_element dash"></li>
						<li class="control_element dots"></li> -->
					</ul>
					<img style="width: 100%; height: 100%" src={image_url} alt="" />
				{/if}
				<div class="loader">
					<div class="blobs">
						<div class="blob-center" />
						<div class="blob" />
						<div class="blob" />
						<div class="blob" />
						<div class="blob" />
						<div class="blob" />
						<div class="blob" />
					</div>
					<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
						<defs>
							<filter id="goo">
								<feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
								<feColorMatrix
									in="blur"
									mode="matrix"
									values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"
									result="goo"
								/>
								<feBlend in="SourceGraphic" in2="goo" />
							</filter>
						</defs>
					</svg>
				</div>

				<!-- <ul class="gallery_prev">
					<li class="gallery_rev_eleme"></li>
					<li class="gallery_rev_eleme"></li>
					<li class="gallery_rev_eleme"></li>
					<li class="gallery_rev_eleme"></li>
					<li class="gallery_rev_eleme prevs_gallery"></li>
				</ul> -->
			</div>
		</div>
	</div>
</div>

<style>
	.ration_list {
		display: flex;
		flex-direction: row;
		gap: 12px;

		align-items: center;
		padding: 0px;
	}

	.ration_element {
		padding: 8px 22px;

		/* height: 32px; */
		box-sizing: content-box;

		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		gap: 8px;

		border-radius: 22px;

		flex: 1;

		color: #8d8d8d;
		border: 1px solid #474747;

		cursor: pointer;

		margin-right: 0px !important;
	}

	.negative-from {
		display: none;
	}

	.negative-from.enable {
		display: flex;
	}

	.ration_element:has(> input:checked) {
		border-color: #8d8d8d;
	}

	.ration_element input {
		display: none;
	}

	.ration_element:hover {
		color: #dedede;
		border-color: #8d8d8d;
	}

	.ration_element .ratio_image {
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;

		width: 26px;
		height: 18px;

		/* background-color: #898989; */

		border-radius: 6px;

		border: 1px solid #898989;
	}

	/* .ration_element.4_3 .ration_image{

	}

	.ration_element.1_1 .ration_image{

	}

	.ration_element.16_9 .ration_image{

	} */

	.radio_list {
		width: 100%;
		height: fit-content;
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 20px;
		overflow-x: auto; /* Добавляем прокрутку */

		margin-top: 14px;
	}

	.radio_list .radio_element {
		width: 200px; /* Устанавливаем фиксированную ширину */
		height: 210px;
		border: 1px solid #262626;
		border-radius: 18px;
		color: #898989;
		box-sizing: border-box;
		padding: 12px;
		flex: 0 0 auto;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		gap: 10px;

		transition: all 0.3s ease-in;

		color: #898989;

		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */

		cursor: pointer;
	}

	.radio_list .radio_element:hover {
		background-color: #191919;
	}

	.radio_list::-webkit-scrollbar {
		display: none;
	}

	.radio_example {
		background-position: center;
		background-size: cover;
		background-repeat: no-repeat;
		border-radius: 18px;

		width: 100%;
		height: 150px;
	}

	.radio_example.realistic {
		background-image: url('https://miro.medium.com/v2/resize:fit:896/1*_j8zrFEzVG5iROChZrtYkQ.png');
	}

	.radio_example.anime {
		background-image: url('https://img.freepik.com/free-photo/anime-style-character-in-space_23-2151134100.jpg');
	}

	.radio_example.impasto {
		background-image: url('https://www.oldholland.com/wp-content/uploads/2019/09/Impasto-2.jpg');
	}

	.radio_example.scifi {
		background-image: url('https://i.pinimg.com/736x/07/ef/1a/07ef1a1d9c3b88efd201961a5fc156fd.jpg');
	}

	.radio_list .radio_element input {
		display: none;
	}

	.radio_list .radio_element:has(input:checked) {
		border: 1px solid #c2c2c2;
		color: #c2c2c2;
		background-color: #343434;
	}

	.toggle_element input[type='checkbox'] {
		height: 0;
		width: 0;
		visibility: hidden;

		display: none;
	}

	.toggle_element label {
		cursor: pointer;
		text-indent: -9999px;
		width: 40px;
		height: 20px;
		background: rgb(65, 65, 65);
		display: block;
		border-radius: 100px;
		position: relative;
	}

	.toggle_element label:after {
		content: '';
		position: absolute;
		top: 5px;
		left: 5px;
		width: 10px;
		height: 10px;
		background: #fff;
		border-radius: 90px;
		transition: 0.3s;
	}

	.toggle_element input:checked + label {
		background: white;
	}

	.toggle_element input:checked + label:after {
		left: calc(100% - 5px);
		transform: translateX(-100%);
		background-color: #262626;
	}

	.toggle_element label:active:after {
		width: 28px;
	}

	.placeholder_generated {
		width: 70%;
		height: 100%;

		border-radius: 22px;

		position: relative;

		background-color: #252525;
	}

	.placeholder_generated.animation {
		animation: flicker 4s infinite;
	}

	.placeholder_generated.animation .loader {
		display: flex;
	}

	.placeholder_generated .loader {
		display: none;

		flex-direction: column;
		align-items: center;
		justify-content: center;

		height: 100%;
	}

	/* .placeholder_generated.animation{
		display: none;
	} */

	.gallery_prev {
		width: 680px;
		height: fit-content;
		padding: 20px;

		box-sizing: content-box;

		display: flex;
		flex-direction: row;
		gap: 20px;

		border-radius: 20px;

		background-color: #4a4a4a17;

		position: absolute;
		bottom: 20px;
		left: calc(50% - 340px);
	}

	.gallery_prev .gallery_rev_eleme {
		width: 120px;
		height: 120px;

		border-radius: 16px;

		background-image: url('https://www.onlandscape.co.uk/wp-content/uploads/2023/02/timparkin_collage_composite_landscape_c209c0c0-18fd-4919-8efd-744fb451e9b8.jpg');
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;

		cursor: pointer;
	}

	.gallery_prev .gallery_rev_eleme:hover {
		opacity: 0.75;
	}

	.gallery_prev .gallery_rev_eleme.prevs_gallery {
		background-image: url('https://img.icons8.com/?size=256&id=RiINzCcRRibi&format=png');
		background-size: 45%;
		filter: invert(100%);
		background-color: #c0c0c0;
	}

	@keyframes flicker {
		0%,
		100% {
			background-color: #252525;
		}
		25%,
		75% {
			background-color: #343434;
		}
		50% {
			background-color: #252525;
		}
	}

	@import url(https://fonts.googleapis.com/css?family=Lato:400,300);

	input[type='radio'] {
		display: none;
	}
	/* input[type='radio']:checked + label span {
		transform: scale(1.25);
	} */
	input[type='radio']:checked + label .red {
		border: 2px solid #711313;
	}
	input[type='radio']:checked + label .orange {
		border: 2px solid #873a08;
	}
	input[type='radio']:checked + label .yellow {
		border: 2px solid #816102;
	}
	input[type='radio']:checked + label .olive {
		border: 2px solid #505a0b;
	}
	input[type='radio']:checked + label .green {
		border: 2px solid #0e4e1d;
	}
	input[type='radio']:checked + label .teal {
		border: 2px solid #003633;
	}
	input[type='radio']:checked + label .blue {
		border: 2px solid #103f62;
	}
	input[type='radio']:checked + label .violet {
		border: 2px solid #321a64;
	}
	input[type='radio']:checked + label .purple {
		border: 2px solid #501962;
	}
	input[type='radio']:checked + label .pink {
		border: 2px solid #851554;
	}

	label {
		display: inline-block;
		width: 25px;
		height: 25px;
		/* margin-right: 10px; */
		cursor: pointer;
	}
	label:hover span {
		opacity: 0.6;
	}
	label span {
		display: block;
		width: 100%;
		height: 100%;
		transition: transform 0.2s ease-in-out;
		border-radius: 20px;
	}
	label span.red {
		background: #db2828ae;
	}
	label span.orange {
		background: #f2711cae;
	}
	label span.yellow {
		background: #fbbd08ae;
	}
	label span.olive {
		background: #b5cc18ae;
	}
	label span.green {
		background: #21ba45ae;
	}
	label span.teal {
		background: #00b5adae;
	}
	label span.blue {
		background: #2185d0ae;
	}
	label span.violet {
		background: #6435c9ae;
	}
	label span.purple {
		background: #a333c8ae;
	}
	label span.pink {
		background: #e03997ae;
	}

	.palette_container {
		gap: 10px;
		justify-content: flex-start;
	}

	.drop-zone {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 18px;

		border: 2px dashed #c2c2c2;
		border-radius: 22px;

		height: fit-content;
		padding: 30px;

		margin-top: 26px;

		background-color: #303030;
	}

	.drop-zone_image {
		background-image: url('https://img.icons8.com/?size=512&id=S9O6fi2ERz41&format=png');
		background-size: cover;
		background-position: center;
		background-repeat: no-repeat;

		width: 60px;
		height: 60px;

		filter: invert(100%);
	}

	.drop-zone_text {
		font-size: 14px;
		line-height: 22px;
		font-weight: 400;
		color: #d7d7d7;

		text-align: center;
	}

	.drop-zone_text span {
		font-weight: 600;
		display: inline-block;

		color: #f3f3f3;

		height: fit-content;
		width: fit-content;
	}

	.control_panel {
		position: absolute;
		top: 20px;
		left: calc(50% - 120px);

		display: flex;
		flex-direction: row;
		align-items: center;

		gap: 24px;

		padding: 16px 32px;

		box-sizing: content-box;
		border-radius: 20px;
		background-color: rgb(60, 60, 60);
		border: 1px solid #39393960;
	}

	.control_element {
		width: 42px;
		height: 42px;

		border-radius: 18px;

		background-position: center;
		background-repeat: no-repeat;
		background-size: 50%;
		background-color: #d7d7d7;

		filter: invert(100%);

		box-sizing: border-box;

		cursor: pointer;

		transition: all 0.2s ease-in-out;
	}

	.control_element:hover {
		background-color: #bababa;
	}

	.control_element.save {
		background-image: url('https://img.icons8.com/?size=512&id=V3lm0b8VZNQK&format=png');
	}

	.control_element.retry {
		background-image: url('https://img.icons8.com/?size=512&id=TLtHYXELMmhb&format=png');
	}

	.control_element.settings {
		background-image: url('https://img.icons8.com/?size=512&id=4511GGVppfIx&format=png');
	}

	.control_element.delete {
		background-image: url('https://img.icons8.com/?size=256&id=KPhFC2OwpbWV&format=png');
	}

	.control_element.dash {
		background-image: url('https://img.icons8.com/?size=256&id=sUJRwjfnGwbJ&format=png');
	}

	.control_element.dots {
		background-image: url('https://img.icons8.com/?size=256&id=16252&format=png');
	}

	.blobs {
		filter: url(#goo);
		width: 300px;
		height: 300px;
		position: relative;
		overflow: hidden;
		border-radius: 70px;
		transform-style: preserve-3d;
	}
	.blobs .blob-center {
		transform-style: preserve-3d;
		position: absolute;
		background: #8fe1ff;
		top: 50%;
		left: 50%;
		width: 30px;
		height: 30px;
		transform-origin: left top;
		transform: scale(0.9) translate(-50%, -50%);
		animation: blob-grow linear 3.4s infinite;
		border-radius: 50%;
		box-shadow: 0 -10px 40px -5px #8fe1ff;
	}
	.blob {
		position: absolute;
		background: #8fe1ff;
		top: 50%;
		left: 50%;
		width: 30px;
		height: 30px;
		border-radius: 50%;
		animation: blobs ease-out 3.4s infinite;
		transform: scale(0.9) translate(-50%, -50%);
		transform-origin: center top;
		opacity: 0;
	}
	.blob:nth-child(1) {
		animation-delay: 0.2s;
	}
	.blob:nth-child(2) {
		animation-delay: 0.4s;
	}
	.blob:nth-child(3) {
		animation-delay: 0.6s;
	}
	.blob:nth-child(4) {
		animation-delay: 0.8s;
	}
	.blob:nth-child(5) {
		animation-delay: 1s;
	}
	@keyframes blobs {
		0% {
			opacity: 0;
			transform: scale(0) translate(calc(-330px - 50%), -50%);
		}
		1% {
			opacity: 1;
		}
		35%,
		65% {
			opacity: 1;
			transform: scale(0.9) translate(-50%, -50%);
		}
		99% {
			opacity: 1;
		}
		100% {
			opacity: 0;
			transform: scale(0) translate(calc(330px - 50%), -50%);
		}
	}
	@keyframes blob-grow {
		0%,
		39% {
			transform: scale(0) translate(-50%, -50%);
		}
		40%,
		42% {
			transform: scale(1, 0.9) translate(-50%, -50%);
		}
		43%,
		44% {
			transform: scale(1.2, 1.1) translate(-50%, -50%);
		}
		45%,
		46% {
			transform: scale(1.3, 1.2) translate(-50%, -50%);
		}
		47%,
		48% {
			transform: scale(1.4, 1.3) translate(-50%, -50%);
		}
		52% {
			transform: scale(1.5, 1.4) translate(-50%, -50%);
		}
		54% {
			transform: scale(1.7, 1.6) translate(-50%, -50%);
		}
		58% {
			transform: scale(1.8, 1.7) translate(-50%, -50%);
		}
		68%,
		70% {
			transform: scale(1.7, 1.5) translate(-50%, -50%);
		}
		78% {
			transform: scale(1.6, 1.4) translate(-50%, -50%);
		}
		80%,
		81% {
			transform: scale(1.5, 1.4) translate(-50%, -50%);
		}
		82%,
		83% {
			transform: scale(1.4, 1.3) translate(-50%, -50%);
		}
		84%,
		85% {
			transform: scale(1.3, 1.2) translate(-50%, -50%);
		}
		86%,
		87% {
			transform: scale(1.2, 1.1) translate(-50%, -50%);
		}
		90%,
		91% {
			transform: scale(1, 0.9) translate(-50%, -50%);
		}
		92%,
		100% {
			transform: scale(0) translate(-50%, -50%);
		}
	}
</style>
