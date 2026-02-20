async function *file_iterator() {
	let page = 1
	let files = []
	do {
		files = await fetch(`${STORAGE_ENDPOINT}?page=${page}`).then(e => e.json())
		for(const f of files) {
			yield f
		}
		page++;
	} while(files.length)
}

function make_node_from_file(file) {
	if(file.mime.includes("video")) return document.createElement("video")
	if(file.mime.includes("image")) return document.createElement("img")
}

async function render(root) {
	for await(const file of file_iterator()) {
		const node = make_node_from_file(file)
		node.src = file.url
		console.log(node)
		root.appendChild(node)
	}
}

async function config() {
	const config = await fetch(STORAGE_ENDPOINT_CONFIG).then(e => e.json())

	upload_input.accept = config.accept
}

(async function() {
	await config()
	await render(container)
})()
