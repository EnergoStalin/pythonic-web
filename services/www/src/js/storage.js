import { STORAGE_FILES_ENDPOINT } from "./endpoints.js"


export async function *file_iterator(limit = 2) {
  let page = 1
  // @type
  let files = []
  do {
    /** @type {{ name: string, mime: string, url: string }[]} */
      files = await fetch(`${STORAGE_FILES_ENDPOINT}?page=${page}&limit=${limit}`).then(e => e.json())
    for(const f of files) {
      yield f
    }
    page++;
  } while(files.length)
}
