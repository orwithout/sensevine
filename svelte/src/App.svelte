<script>
	let links = [
	  'http://4.193.54.245:8002/Dw4XJS91m0FAnGdC/hello.py/read',
	  'http://4.193.54.245:8002/Dw4XJS91m0FAnGdC/hello.py/run?params=嗨0o0'

	];
  
	let results = {};
  	let timeouts = {};
  	let customUrl = 'http://4.193.54.245:8002/Dw4XJS91m0FAnGdC/list';
  	let customUrl2 = 'http://4.193.54.245:8002/Dw4XJS91m0FAnGdC/chat.py/run?params=你好啊,可以为我写一首深圳这座城市的夜景的诗吗？我刚在飞机上飞过了深圳夜晚的上空，太每妙、太震撼了';
	let customUrl3 = 'http://4.193.54.245:8002/Dw4XJS91m0FAnGdC';
	let currentResult = 'Awaiting response...';  // 新添加的变量

  	async function fetchApi(url, file) {
		const formData = new FormData();
		if (file) {
			formData.append('file', file);
		}
	   
	  	try {
			// Set a timeout to check for no response
			timeouts[url] = setTimeout(() => {
				results[url] = "No response.";
			}, 5000);  // 5 seconds timeout
			
			const response = await fetch(url, {
				method: file ? 'POST' : 'GET',  // 使用 POST 方法如果有文件需要上传
				body: file ? formData : null
			});
			clearTimeout(timeouts[url]);  // Clear the timeout if response received
			
			if (!response.ok) {
				results[url] = "Error: " + response.status;
				return;
			}
			
			const data = await response.text();
			results[url] = data || "No data received.";
	  	} catch (error) {
			results[url] = "An error occurred: " + error.message;

	  	}
	  	currentResult = results[url] || "An error occurred.";
	}

	function uploadFile() {
		const fileInput = document.getElementById("fileInput");
		const file = fileInput.files[0];
		let finalUrl = customUrl3 + "/upload";  // 拼接 "/upload"
		if (file) {
			fetchApi(finalUrl, file);
		} else {
			results['upload'] = 'No file selected';
		}
	}

</script>



<style>
	.button-list {
		display: flex;
		flex-direction: column;  /* 竖向排列 */
		gap: 10px;  /* 按钮之间的间距 */
		width: 550px;  /* 你可以修改这个值 */
	}
	
	.input-container {
		margin-top: 20px;
	}

	textarea {
		width: 550px;
		height: 100px;
	}

	input {
		width: 550px;  /* 你可以修改这个值 */
	}
</style>



<main>
	<div class="container">
		<!-- 操作区 -->
		<div class="operation-column">

			<div class="button-list">  <!-- 新添加的 div 用于竖向排列按钮 -->
				{#each links as link}
				<button on:click={() => fetchApi(link)}>{link}</button>
				{/each}
			</div>

			<div class="upload-container">
				<input type="file" id="fileInput" />
				<input type="text" id="urlInput" bind:value={customUrl3}  placeholder="Enter custom URL for upload" />
				<button on:click={uploadFile}>上传</button>
			</div>
			
			<div class="input-container">
				<input bind:value={customUrl} placeholder="Enter custom URL" />
				<button on:click={() => fetchApi(customUrl)}>请求</button>
			</div>
			
			<div class="input-container">
				<textarea bind:value={customUrl2} placeholder="Enter custom URL"></textarea>
				<button on:click={() => fetchApi(customUrl2)}>询问</button>
			</div>

		</div>

		<!-- 结果输出区 -->
		<div class="result-column">
			<div class="result">
				{currentResult}  <!-- 使用新的 currentResult 变量 -->
			</div>
		</div>

	</div>
</main>
