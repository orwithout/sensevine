<script>
	let links = [
	  'http://api.sensevine.com/1234567/public-test/hello.py/read',
	  'http://api.sensevine.com/1234567/public-test/hello.py/run?params=嗨0o0'
	];
	let results = {};
  	let timeouts = {};
  	let customUrl = 'http://api.sensevine.com/1234567/public-test/list';
  	let customUrl2 = 'http://api.sensevine.com/1234567/public-test/chat.py/run?params=你好啊,可以为我写一首深圳这座城市的夜景的诗吗？我刚在飞机上飞过了深圳夜晚的上空，太美妙、太震撼了';
	let customUrl3 = 'http://api.sensevine.com/1234567/public-test';
	let currentResult = '待命...';  // 新添加的变量


async function fetchApi(url, file) {
    const formData = new FormData();
    if (file) {
        formData.append('file', file);
    }

    try {
        // Set a timeout to check for no response
        timeouts[url] = setTimeout(() => {
            currentResult = "No response.";
            console.log("Timeout:", currentResult);  // 输出到控制台
        }, 5000);  // 5 seconds timeout
        
        const response = await fetch(url, {
            method: file ? 'POST' : 'GET',  // 使用 POST 方法如果有文件需要上传
            body: file ? formData : null
        });

        clearTimeout(timeouts[url]);  // Clear the timeout if response received

        if (!response.ok) {
            currentResult = "Error: " + response.status;
            console.log("Response Error:", currentResult);  // 输出到控制台
            return;
        }
        
        const data = await response.text();
        currentResult = data || "No data received.";
        console.log("Response Data:", currentResult);  // 输出到控制台
    } catch (error) {
        currentResult = "An error occurred: " + error.message;
        console.log("Catch Block:", currentResult);  // 输出到控制台
    }
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
		align-items: flex-start;  /* 内容靠左对齐 */
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
				<button on:click={() => fetchApi(customUrl)}>访问</button>
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
				<button on:click={() => currentResult = '待命...'}>刷新</button>
			</div>
		</div>
	</div>
</main>

<div style="display: flex; align-items: center;">
	<img id="imageToHide" src='image.gif' alt="senseVine.com dancing" />
	<button on:click={(e) => e.target.previousElementSibling.style.display = 'none'}>关闭</button>
</div>
  
  