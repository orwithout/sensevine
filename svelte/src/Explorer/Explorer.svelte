<script>
	import { createEventDispatcher } from 'svelte';
	import { slide } from 'svelte/transition';
	
	// export let type;
	export let columnIndex;
	export let folderIndex;
	export let name;
	export let path;
	export let files = null;
	export let selected_folder_icon = false;
	export let selected_file_icon = false;
	export let selected_name = false;  // 新增
	let type = name && name.slice(name.lastIndexOf('.') + 1); // 用于文件类型

	const dispatch = createEventDispatcher();


	function select_icon() {
		if (files) {
			selected_folder_icon = !selected_folder_icon;
		} else {
			selected_file_icon = !selected_file_icon;
		}
	}

	// function select_name() {
	// 	selected_name = !selected_name;
	// 	if (!files) {
	// 		dispatch('folderclick', { name });
	// 	} else {
	// 		dispatch('folderclick', { name, files });
	// 	}
	// }

	async function select_name() {
		selected_name = !selected_name;
		dispatch('folderclick', { columnIndex, folderIndex, path, name, selected_name, selected_folder_icon });
		console.log("Explorer.folderclick:", JSON.stringify(name));
	}


	import { onMount } from "svelte";
	let fileIcon = `/icons/file-type-${type}.svg`;
	onMount(() => {
		let img = new Image();
		img.src = fileIcon;
		img.onerror = function() {
			fileIcon = '/icons/file-type-.svg';
		}
	});



</script>



<!-- 文件夹或文件逻辑 -->
<button
    on:click={select_icon}
    on:keydown={event => {if (event.key === 'Space') select_icon()}}
    class="button-base icon-button"
    class:selected_folder_icon={selected_folder_icon}
    class:selected_file_icon={selected_file_icon}>
    {#if files}
        <span class="folder-icon"></span>
    {:else}
        <span class="file-icon" style="background-image: url({fileIcon});"></span>
    {/if}
</button>



<button
    on:click={select_name}
    on:keydown={event => {if (event.key === 'Space') selected_name()}}
    class="button-base name-button"
    class:selected_name={selected_name}>
    <span>{name}</span>
</button>


{#if files && selected_folder_icon}
	<ul transition:slide={{ duration: 144 }}>
        {#each files as file}
            <li>
                <svelte:self {...file} on:folderclick={e => dispatch('folderclick', e.detail)} />
            </li>
        {/each}
    </ul>
{/if}







<style>
    /* Base styles */
    .button-base {
        border: none;
        background: none;
        padding: 0 0 0 0;
        margin: 0 0 0 0;
        line-height: 0;
        cursor: pointer;
        display: inline-flex;
        flex-shrink: 0;
        align-items: center;
    }

    .icon-button .folder-icon {
        background: url(/icons/folder.svg) 0 0.2em no-repeat;
        background-size: 1.6em 1.6em;
        width: 1.6em;
        height: 1.6em;
    }
    .icon-button.selected_folder_icon .folder-icon {
        background-image: url(/icons/folder-open.svg);
    }




	.icon-button .file-icon {
        /* background: url(/icons/file-type-{type}.svg) 0 0.1em no-repeat; 不支持外部样式使用变量,只能使用内联样式*/
    	/* background-image: url('/icons/file-type-.svg'), url('/icons/file-type-{type}.svg'); */
		
		background-size: 1em 1em;
        width: 1em;
        height: 1em;
    }
    .icon-button.selected_file_icon .file-icon {
        background-color: #b4b4b4;
    }

    /* Folder and File Name Buttons */
    .name-button {
		/* padding: 0 0 0 0; */
        margin: 0 2.6em 0 0; /*  每列的文字后面添加空格 */
        font: inherit;
        font-weight: bold;
        font-size: 14px;
    }
    .name-button.selected_name {
        background-color: #b4b4b4;
    }






    /* List styles */
    ul {
		padding: 0 0 0 1.2em;  /* 与下面 margin 一起可以觉得图标与文字之间距离*/
        margin: 0 0 0 0.4em;
		list-style: none;
        border-left: 1px solid #eee;
    }
    /* li {
        padding: 0 0.5em 0 0.5em;
        margin: 0 0.5em 0 0.5em;
    } */
</style>
