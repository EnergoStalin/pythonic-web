const BASE_URL = "http://127.0.0.1:7727";

const JOURNAL_ENDPOINT = `${BASE_URL}/journal`;

const AUTH_ENDPOINT = `${BASE_URL}/auth`;

/*
	{ GET
		"validation": {
			"fio": { "regex": "", description: "" },
			"password": { "regex": "", description: "" }
		}
	}
*/
const AUTH_CONFIG_ENDPOINT = `${AUTH_ENDPOINT}/config`;

/*
	[ GET paging with &page until empty array returned
		{
			"name": "",
			"mime": ""
		}
	]
*/
const STORAGE_ENDPOINT = `${BASE_URL}/storage`

/*
	{ GET
		"accept": ".mp4,.png"
	}
*/
const STORAGE_ENDPOINT_CONFIG = `${STORAGE_ENDPOINT}/config`

const USER_ENDPOINT = `${BASE_URL}/user`;
