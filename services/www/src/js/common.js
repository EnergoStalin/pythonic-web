import { BASE_URL } from "./endpoints.js";

export function update_form_action() {
  for(const f of document.forms) {
    f.action = new URL(new URL(f.action).pathname, BASE_URL).toString()
  }
}
