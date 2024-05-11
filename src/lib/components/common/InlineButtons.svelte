<script>
	import { onMount, getContext } from 'svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	const i18n = getContext('i18n');

	export let buttons = [];
	export let name = null;
	export let fit = null;

	let selectedButton = buttons[0].text || null; // Инициализируем selectedButton значением первого элемента массива buttons или null, если массив пустой

	// Функция для обработки выбора кнопки
	function handleButtonClick(event, value) {
		event.stopPropagation();
		event.preventDefault();

		console.log(value)

		selectedButton = value;
	}
</script>

<div class="button-row rounded-full">
	{#each buttons as button}
		{#if fit == true}
			<label
				class={`rounded-3xl ${fit == true ? 'full' : ''} ${
					selectedButton === button.text ? 'button' : ''
				}`}
				on:click={(event) => handleButtonClick(event, button.text)}
			>
				<Tooltip styling={'position: absolute; top: -6px; left: 0; width: 100%; height: 100%;'} content={$i18n.t(button.tooltip)}>
					<input name="inline_{name}" type="radio" bind:value={button.text} />
				</Tooltip>
				{button.text}
			</label>
		{:else}
			<label
				class={`rounded-3xl ${fit == true ? 'full' : ''} ${
					selectedButton === button ? 'button' : ''
				}`}
				on:click={handleButtonClick}
			>
				<input name="inline_{name}" type="radio" bind:value={button} />
				{button}
			</label>
		{/if}
	{/each}
</div>

<style>
	.button-row {
		display: flex;
		align-items: center;
		border: 1px solid rgba(70, 70, 70, 0.735);
		background-color: #282828;

		gap: 4px;

		padding: 6px;
	}

	.button-row:has(> .full) {
		gap: 12px;
	}

	.button-row label {
		font-size: 14px;
		line-height: 24px;

		padding: 4px 24px;

		transition: all 0.3s ease-in-out;

		color: white;
		background-color: rgba(222, 222, 222, 0);

		cursor: pointer;
	}

	.button-row label:hover {
		background-color: rgba(222, 222, 222, 0.15);
	}

	.button-row label.button {
		background-color: rgba(222, 222, 222, 0.9);

		color: black;
	}

	.button-row .full {
		width: 100%;
		text-align: center;

		font-size: 16px;
		line-height: 28px;

		position: relative;
	}

	.button-row .full > div{
		position: absolute;
		top: 0;
		left: 0;

		width: 100%;
		height: 100%;
	} 

	.button-row label.button:hover {
		background-color: rgba(222, 222, 222, 0.7);
	}

	input[type='radio'] {
		display: none;
	}

	/* .button {
      padding: 10px;
      border: 1px solid #ccc;
      cursor: pointer;
    }
  
    .button.selected {
      background-color: lightblue;
    } */
</style>
