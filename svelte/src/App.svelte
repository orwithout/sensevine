<script>
	import { onMount } from 'svelte';
	import 'jstree/dist/themes/default/style.min.css';
	import 'jstree';
  
	let treeData = [];
  
	onMount(() => {
	  loadData();
	});
  
	async function loadData() {
	  try {
		const response = await fetch(`https://api.sensevine.com/list-dir/`);
		if (!response.ok) {
		  throw new Error(`HTTP error! status: ${response.status}`);
		}
		const data = await response.json();
		treeData = data.items.map((item, index) => ({ 
		  id: `/${item}`, 
		  text: item, 
		  children: true 
		}));
		console.log("Tree data:", treeData);
  
		// 初始化 jsTree
		initTree();
	  } catch (error) {
		console.error("Failed to fetch data:", error);
	  }
	}
  
	function initTree() {
	  window.$('#tree').jstree({
		'core': {
		  'data': treeData
		}
	  });
	}
  </script>
  
  
  <div id="tree"></div>
  
  <style>
	#tree {
	  width: 300px;
	  height: 300px;
	}
  </style>
  



