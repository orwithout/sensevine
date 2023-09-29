<script>
	import Explorer from './Explorer/Explorer.svelte';
	let root = [
		{
			type: 'folder',	name: '@灰面',
			files: [
				{
					type: 'folder', name: '登录',
					files: [
						{
							type: 'folder', name: '登录方式管理',
							files: [
								{ type: 'file', name: '电子邮箱.json' },
								{ type: 'file', name: '微信扫码.json' },
								{ type: 'file', name: '.新建.senseurl.com.py' }
							]
						},
						{ type: 'file', name: '.登录.senseurl.com.py' },
						{ type: 'file', name: '.注销.senseurl.com.py' }
					]
				},
				{
					type: 'folder', name: '留言',
					files: []
				},
				{
					type: 'folder', name: '群组',
					files: []
				},
				{
					type: 'folder', name: '私信',
					files: []
				}
			]
		},
		{
			type: 'folder',	name: '探索', files: []
		},
		{
			type: 'folder',	name: '通讯录',
			files: [
				{
					type: 'folder', name: '关注',
					files: [
						{
							type: 'folder', name: '增醉墨' ,
							files: [
								{ type: 'folder', name: '主人信息', files: [] },
								{ type: 'folder', name: '群组', files: [] },
								{ type: 'folder', name: '探索', files: [] },
								{ type: 'file', name: '.RSS订阅拉取.senseurl.com.py'},
								{ type: 'file', name: '.新建.senseurl.com.py'},
							]
						},
						{ type: 'folder', name: '同其尘' , files: [] },
						{ type: 'folder', name: '飒' , files: [] }
					]
				},
				{
					type: 'folder', name: '被关注',
					files: [
						{ type: 'folder', name: '同其尘' , files: [] },
						{ type: 'folder', name: '飒' , files: [] }
					]
				},
				{
					type: 'folder', name: '黑名单',
					files: [
						{ type: 'folder', name: '鸡毛令箭' , files: [] },
						{ type: 'folder', name: '和尚' , files: [] }
					]
				}
			]
		},
		{ type: 'file', name: 'id.auth' },
		{ type: 'file', name: 'id.email' },
		{ type: 'file', name: 'id.hard' },
		{ type: 'file', name: 'JWT.json' },
		{ type: 'file', name: 'senseurl.py' },
		{ type: 'file', name: 'senseurl0.py' }
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
				<Explorer name="senseurl.com" files={ROW} expanded />
			</div>
		{/each}
	</div>
	{/each}
</div>

