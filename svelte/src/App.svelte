<script>
	import Explorer from './Explorer/Explorer.svelte';
	let root = [
		{
			type: 'folder',
			name: 'Important work stuff',
			files: [{ type: 'file', name: 'quarterly-results.xlsx' }]
		},
		{
			type: 'folder',
			name: 'Animal GIFs',
			files: [
				{
					type: 'folder',
					name: 'Dogs',
					files: [
						{ type: 'file', name: 'treadmill.gif' },
						{ type: 'file', name: 'rope-jumping.gif' }
					]
				},
				{
					type: 'folder',
					name: 'Goats',
					files: [
						{ type: 'file', name: 'parkour.gif' },
						{ type: 'file', name: 'rampage.email' }
					]
				},
				{ type: 'file', name: 'cat-roomba.gif' },
				{ type: 'file', name: 'duck-shuffle.gif' },
				{ type: 'file', name: 'monkey-on-a-pig.gif' }
			]
		},
		{ type: 'file', name: 'TODO.md' }
	];

	let ROWS = [root, root, root, root, root, root, root, root];
	let COLUMNS = [root,root, root, root, root];

</script>



<style>
	.rows-container {
		display: flex;
		white-space: nowrap;
		/* flex-direction: column;  竖向排列 */
	}
	.columns-container {
		flex-direction: column;  /* 竖向排列*/
	}

</style>



<main>
</main>

<div class="rows-container">
	{#each ROWS as ROW}
	<div class="columns-container">
		{#each COLUMNS as COLUMN}
			<div class="columns-container">
				<Explorer name="Home" files={ROW} expanded />
			</div>
		{/each}
	</div>
	{/each}
</div>

