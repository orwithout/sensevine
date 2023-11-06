<script>


  	export let name = "Default Name";
  	export let files = [];

  	import { onMount } from 'svelte';


    onMount(() => {
        console.log("Explorer mounted with:", { name, files });
    });
</script>





<div>
    Name: {name}
    Files: {JSON.stringify(files, null, 2)}
</div>
