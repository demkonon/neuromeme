<script lang="ts">
	import { writable } from 'svelte/store';
	import { toast } from 'svelte-sonner';
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { onMount, getContext } from 'svelte';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import ButtonRow from '$lib/components/common/InlineButtons.svelte';
	import DropSelector from '$lib/components/common/DropSelector.svelte';

  	let buttons = ['Personal', 'Community', 'Collections'];
	let chatTextAreaElement: HTMLTextAreaElement;
	let chatInputPlaceholder = '';


	const i18n = getContext('i18n');

	const images_array = [
		'https://source.unsplash.com/bYuI23mnmDQ',
		'https://source.unsplash.com/Nllx4R-2c3o',
		'https://source.unsplash.com/lp40q07DIe0',
		'https://source.unsplash.com/wfalq01jJuU',
		'https://source.unsplash.com/rMHNK_skwwU',
		'https://source.unsplash.com/WBMjuGpbrCQ',
		'https://source.unsplash.com/nCUZ5BYBL_o',
		'https://source.unsplash.com/3u4fzMQZhjc',
		'https://source.unsplash.com/bYuI23mnmDQ',
		'https://source.unsplash.com/Nllx4R-2c3o',
		'https://source.unsplash.com/lp40q07DIe0',
		'https://source.unsplash.com/wfalq01jJuU',
		'https://source.unsplash.com/rMHNK_skwwU',
		'https://source.unsplash.com/WBMjuGpbrCQ',
		'https://source.unsplash.com/nCUZ5BYBL_o',
		'https://source.unsplash.com/3u4fzMQZhjc',
		'https://source.unsplash.com/bYuI23mnmDQ',
		'https://source.unsplash.com/Nllx4R-2c3o',
		'https://source.unsplash.com/lp40q07DIe0',
		'https://source.unsplash.com/wfalq01jJuU',
		'https://source.unsplash.com/rMHNK_skwwU',
		'https://source.unsplash.com/WBMjuGpbrCQ',
		'https://source.unsplash.com/nCUZ5BYBL_o',
		'https://source.unsplash.com/3u4fzMQZhjc',
		'https://source.unsplash.com/bYuI23mnmDQ',
		'https://source.unsplash.com/Nllx4R-2c3o',
		'https://source.unsplash.com/lp40q07DIe0',
		'https://source.unsplash.com/wfalq01jJuU',
		'https://source.unsplash.com/rMHNK_skwwU',
		'https://source.unsplash.com/WBMjuGpbrCQ',
		'https://source.unsplash.com/nCUZ5BYBL_o',
		'https://source.unsplash.com/3u4fzMQZhjc',
	]

	const tags = [
		{
			name: '✨ new',
			color: '#7a4579'
		},
		{
			name: '🔥 hot',
			color: '#686ee2'
		},
		{
			name: '👑 realistic',
			color: '#f16821'
		},
		{
			name: '💢 anime',
			color: '#1a3263'
		},
	]

	export let prompt = '';
	export let submitPrompt: Function;
</script>

<div class="min-h-screen max-h-[100dvh] w-full flex justify-center dark:text-white">
	<div class="flex flex-col justify-between w-full overflow-y-auto">
		<div class="max-w-7xl mx-auto w-full px-3 md:px-0 my-10">
			<div class="mb-6 flex justify-between items-center">
				<!-- <div class=" text-2xl font-semibold self-center">{$i18n.t('Gallery')}</div> -->
				<form
					class=" flex flex-col relative w-[460px] rounded-3xl px-1.5 border border-gray-100 dark:border-gray-850 bg-white dark:bg-gray-900 dark:text-gray-100"
					on:submit|preventDefault={() => {
						console.log(prompt);
					}}
					style="margin-right: auto"
				>
					<div class=" flex" style="width: 100%">
						<textarea
							id="chat-textarea"
							bind:this={chatTextAreaElement}
							class=" dark:bg-gray-900 dark:text-gray-100 outline-none w-full py-3 px-3 rounded-xl resize-none h-[48px]"
							style="border-radius: 14px;"
							placeholder={chatInputPlaceholder !== ''
								? chatInputPlaceholder
								: $i18n.t('Enter search')}
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
								e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
								user = null;
							}}
							on:focus={(e) => {
								e.target.style.height = '';
								e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
							}}
							on:paste={(e) => {
								
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
								{$i18n.t('Search')}
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
				<ButtonRow {buttons}/>
				<div style="margin-left: 20px;">
					<DropSelector
						renameHandler={() => {
							
						}}
						deleteHandler={() => {
							
						}}
						onClose={() => {
							
						}}
					>
						<button
							aria-label="Chat Menu"
							class="dropdown_select self-center"
							on:click={() => {
								
							}}
						>
							Sorting
						</button>
					</DropSelector>
				</div>
			</div>
			<div class="">
				<div
					class="columns-1 gap-5 sm:columns-2 sm:gap-6 md:columns-3 lg:columns-4 [&>div:not(:first-child)]:mt-6"
				>
					{#each images_array.sort(() => Math.random() - 0.5) as image}
						<div class="gallery-item rounded-2xl p-2 pb-4 overflow-hidden relative">
							<img src="{image}" class="relative overflow-hidden rounded-xl w-full h-full" alt="gallery_image"/>
							<div class="flex w-full flex-row align-center gap-2">
								<img loading="lazy"  src="https://imgcdn.stablediffusionweb.com/2024/4/19/6e5de0e8-d9b0-493f-947d-8beac39e0d38.jpg" alt="human_portrait" class="w-[32px] h-[32px] rounded-full">
								<p class="gallery_title">{$i18n.t('Image title')}<span class="gallery_description">{$i18n.t('Some description text about gallery image')}</span></p>
							</div>
							

							<!-- <ul class="tag_list flex align-center justify-between gap-1.5">
								{#each tags.sort(() => Math.random() - 0.5).slice(0, Math.floor(Math.random() * 3) + 1) as tag}
									<li class="tag_element" style="background-color: {tag.color + 'aa'}; border-color: {tag.color}">{$i18n.t(tag.name)}</li>
								{/each}
							</ul> -->

							<span class="gallery-item_like absolute rounded-full w-[36px] h-[36px]">
							</span>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.gallery-item{
		background-color: #68686835;
		text-overflow: ellipsis;
		overflow: hidden;

		cursor: pointer;
	}

	.gallery-item::before{
		position: absolute;
		top: .5rem;
		left: .5rem;

		width: calc(100% - .1rem);
		height: 120px;

		content: '';

		display: block;

		background-image: linear-gradient(to top, rgba(255, 255, 255, 0) 20%, rgba(42, 42, 42, .4) 100%);

		z-index: 2;
		transition: all .6s ease-in-out;

		opacity: 0;

		border-top-left-radius: .75rem;
		border-top-right-radius: .75rem;
	}

	.gallery-item:hover::before{
		opacity: 1;
	}

	div:has(>.gallery_title){
		margin-top: 12px;
		align-items: center;

		padding: 0 12px;
	}

	.gallery_title{
		width: 100%;
		overflow: hidden;
		text-overflow: ellipsis;

		font-size: 18px;
		line-height: 26px;
	}

	.tag_list{
		position: absolute;
		top: 20px;
		right: 20px;

		opacity: .9;

		z-index: 3;
	}

	.tag_element{
		display: block;
		padding: 3px 12px;
		font-size: 12px;
		line-height: 16px;

		border-radius: 20px;

		font-weight: 700px;

		border: 2px solid;
	}

	

	.gallery_description{
		width: 100%;
		line-height: 20px;
		font-size: 14px;

		overflow: hidden;
		text-overflow: ellipsis;
		text-wrap: nowrap;

		display: block;

		color: rgba(255, 255, 255, 0.75);
	}

	.gallery-item:hover .gallery-item_like{
		opacity: 1;
	}

	.gallery-item_like{
		border: 1px solid whtie;

		background-image: url('https://img.icons8.com/?size=512&id=87&format=png');
		background-position: center;
		background-size: 50%;
		background-repeat: no-repeat;
		background-color: white;

		top: 20px;
		right: 20px;

		display: block;
		cursor: pointer;

		z-index: 3;

		opacity: 0;

		transition: all .3s ease-in-out;
	}

	.gallery-item_like:hover{
		opacity: .75;
		background-color: #FBECFA;
	}

</style>