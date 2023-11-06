export async function fetchFileList(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Error fetching file list: " + response.status);
        }
        const data = await response.json();

        // Recursive function to sort content
        function sortContent(content) {
            content.sort((a, b) => {
                if (a.files && !b.files) return -1;
                if (!a.files && b.files) return 1;
                return 0;
            });

            // Continue sorting for nested files
            for (const item of content) {
                if (item.files) {
                    sortContent(item.files);
                }
            }
        }

        // Assuming the content is directly in the data object
        if (data && data.content) {
            sortContent(data.content);
        }

        return data;
    } catch (error) {
        console.error(error);
        return null;
    }
}
