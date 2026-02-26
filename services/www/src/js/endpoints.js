export const BASE_URL = "http://127.0.0.1:7727";

export const JOURNAL_ENDPOINT = `${BASE_URL}/journal`;

export const AUTH_ENDPOINT = `${BASE_URL}/auth`;

/**
 * @typedef {Object} Validation
 * @property {string} regex
 * @property {string} description
 */

/**
	* @typedef {Object} AuthEndpointConfig
	* @property {Record<string, Validation>} validation
	*/
export const AUTH_CONFIG_ENDPOINT = `${AUTH_ENDPOINT}/config`;

/**
 * @typedef {Object} FileItem
 * @property {string} name
 * @property {string} mime
 * @property {string} url
 */

/**
 * @typedef {FileItem[]} GetStorageEndpointResponse
 */
export const STORAGE_ENDPOINT = `${BASE_URL}/storage`

/*
	{ GET
		"accept": ".mp4,.png"
	}
*/
/**
 * @typedef {FileItem[]} GetStorageEndpointConfigResponse
 */
export const STORAGE_ENDPOINT_CONFIG = `${STORAGE_ENDPOINT}/config`

export const USER_ENDPOINT = `${BASE_URL}/user`;
