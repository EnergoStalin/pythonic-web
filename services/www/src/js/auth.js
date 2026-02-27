import { AUTH_CONFIG_ENDPOINT } from "./endpoints.js"

const config = await fetch(AUTH_CONFIG_ENDPOINT).then(e => e.json());

const v = config.validation

login.pattern = v.login.regex
login.pattern = v.login.regex
password_description.textContent = v.password.description
password.pattern = v.password.regex
