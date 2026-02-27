import { update_form_action } from "./common.js";
import { AUTH_CONFIG_ENDPOINT } from "./endpoints.js"

update_form_action()

const config = await fetch(AUTH_CONFIG_ENDPOINT).then(e => e.json());

const v = config.validation

login.pattern = v.login.regex
login.pattern = v.login.regex
password_description.textContent = v.password.description
password.pattern = v.password.regex
