<script>
	import Explorer from './Explorer/Explorer.svelte';
	// export let name;
	let foldersMatrix = [[{
  		'./': ["a", "b", "c", {'abc/': ["d", "e", "f", {}]}]
	}]];




	import { fetchFileList } from './apiMethods.js';

	let base_url = 'https://api.sensevine.com/1234567';
	if (!base_url.endsWith('/')) {
		base_url += '/';
	}



	async function handleFolderClick(event) {
		const folderData = event.detail;

		const response = await fetchFileList(base_url +folderData.path +'list');

		if (response && response.content) {
			console.log("Before updating foldersMatrix:", JSON.stringify(foldersMatrix));
			// updateFoldersMatrix(folderData.columnIndex, folderData.folderIndex, folderData, response);
			// console.log("After updating foldersMatrix:", JSON.stringify(foldersMatrix));
		} else {
			console.error("Failed to update foldersMatrix. Response:", response);
		}
	}







</script>



<style>
	.rows-container {
		display: flex;
		white-space: nowrap;
		/* flex-direction: column;  竖向排列 */
	}
	.column-container {
		flex-direction: column;  /* 竖向排列*/
	}

</style>



<main>
</main>






<!-- <button on:click={handleFolderClick}>Add Column</button> -->



<div class="rows-container">
	{#each foldersMatrix as column, columnIndex}
	<div class="column-container">
	  {#each column as folder, folderIndex}
	  <div class="column-container">
		<Explorer {...folder} columnIndex={columnIndex} folderIndex={folderIndex} selected_folder_icon on:folderclick={handleFolderClick} />
		<!-- <pre>{JSON.stringify(column, null, 2)}</pre> -->
	  </div>
	  {/each}
	</div>
	{/each}
</div>

