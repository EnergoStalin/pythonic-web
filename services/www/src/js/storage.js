import { STORAGE_ENDPOINT } from "./endpoints"


export async function *file_iterator() {
	let page = 1
	// @type
	let files = []
	do {
		/** @type {{ name: string, mime: string, url: string }[]} */
		files = await fetch(`${STORAGE_ENDPOINT}?page=${page}`).then(e => e.json())
		for(const f of files) {
			yield f
		}
		page++;
	} while(files.length)
}
