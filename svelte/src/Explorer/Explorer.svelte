<script>
	import File from './File.svelte';
	import { slide } from 'svelte/transition';
	
	export let expanded = false;
	export let name;
	export let files;
	export let selected = false;  // 新增

	function toggle() {
		expanded = !expanded;
	}

	function select() {   
		selected = !selected;
	}

</script>



<!-- 文件夹图标的按钮 -->
<button 
	on:click={toggle}
	on:keydown={event => {if (event.key === 'Space') toggle()}}
	class="button-base folder-icon-button"
	class:expanded={expanded}>
	<span class="folder-icon"></span>
</button>

<!-- 文件夹名称的按钮 -->
<button 
	on:click={select}
	on:keydown={event => {if (event.key === 'Space') select()}}
	class="button-base folder-name-button"
	class:selected={selected}>
	<span class="folder-name">{name}</span>
</button>






{#if expanded}
	<ul transition:slide={{ duration: 300 }}>
		{#each files as file}
			<li>
				{#if file.type === 'folder'}
					<svelte:self {...file} />
				{:else}
					<File {...file} />
				{/if}
			</li>
		{/each}
	</ul>
{/if}

<style>

.button-base {
    border: none;
    background: none;
    padding: 0;
    margin: 0;
	line-height: 0;
    cursor: pointer;
    display: inline-flex;
	flex-shrink:0;
    align-items: center;
}


.folder-name-button {
	font: inherit;
    font-weight: bold;
	/* min-width: 150px; */
    font-size: 14px;
}

/* .folder-icon-button {

} */



.folder-name-button.selected {
    background-color: #b4b4b4;
}

.folder-icon-button .folder-icon {
    background: url(/icons/folder.svg) 0 0.2em no-repeat;
    background-size: 1em 1em;
    width: 1em;
    height: 1em;
}

.folder-icon-button.expanded .folder-icon {
    background-image: url(/icons/folder-open.svg);
}

ul {
    padding: 0.2em 0 0 0.5em;
    margin: 0 0 0 0.5em;
    list-style: none;
    border-left: 1px solid #eee;
}

li {
    padding: 0.2em 0;
}

</style>






