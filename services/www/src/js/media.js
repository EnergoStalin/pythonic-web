import { update_form_action } from "./common.js"
import { STORAGE_ENDPOINT_CONFIG } from "./endpoints.js"
import { file_iterator } from "./storage.js"

update_form_action()

/**
	* @param {import("./endpoints").FileItem} file
	*/
function make_node_from_file(file) {
	if(file.mime.includes("video")) return document.createElement("video")
	if(file.mime.includes("image")) return document.createElement("img")
}

/**
	* @param {HTMLElement} root
	*/
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

	// @ts-ignore
	upload_input.accept = config.accept
}

await config()

// @ts-ignore
await render(container)
