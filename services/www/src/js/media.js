import { update_form_action } from "./common.js"
import { STORAGE_ENDPOINT_CONFIG, STORAGE_FILES_ENDPOINT } from "./endpoints.js"
import { file_iterator } from "./storage.js"

update_form_action()

function set_disabled(e, v) {
  for (const el of e.elements) {
    el.disabled = v
  }
}

/** @param {import("./endpoints").FileItem} file */
function make_node_from_file(file) {
  if(file.mime.includes("video")) {
    const e = document.createElement("video")
    e.controls = true
    return e
  }
  if(file.mime.includes("image")) return document.createElement("img")
}

/** @param {HTMLElement} root */
async function render(root) {
  for await(const file of file_iterator(20)) {
    const container = document.createElement("div")
    container.innerHTML = `<p>${file.name}</p>`
    const node = make_node_from_file(file)
    if (!node) continue
    node.src = file.url
    container.appendChild(node)
    root.appendChild(container)
  }
}

async function config() {
  const config = await fetch(STORAGE_ENDPOINT_CONFIG).then(e => e.json())

  const form = document.forms[0]
  form.action = STORAGE_FILES_ENDPOINT

  // @ts-ignore
  files.accept = config.accept
  set_disabled(form, false)
}

await config()

// @ts-ignore
await render(container)
document.forms[0].addEventListener("submit", async function(e) {
  e.preventDefault()

  /** @type {HTMLInputElement} */
    const fileInput = document.querySelector("input[type='file']")

  if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    alert("Please select files to upload")
    return
  }

  const data = new FormData()

  for (const file of fileInput.files) {
    data.append(fileInput.name, file, file.name)
  }

  try {
    set_disabled(e.target, true)
    const response = await fetch(STORAGE_FILES_ENDPOINT, {
      method: "POST",
      body: data
    })
    set_disabled(e.target, false)

    if (response.ok) {
      window.location.reload()
    } else {
      const error = await response.text()
      alert(`Upload failed: ${error}`)
    }
  } catch (error) {
    console.error("Upload error:", error)
    alert("Upload failed. Please check your connection.")
  }
})
