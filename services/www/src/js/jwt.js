/**
  * @param {string} token
  */
export function decodeJWT(token) {
	try {
		// Split the token into parts
		const parts = token.split('.');
		if (parts.length !== 3) {
			throw new Error('Invalid JWT token format');
		}

		// Decode the header (first part)
		const header = JSON.parse(atob(parts[0]));

		// Decode the payload (second part)
		const payload = JSON.parse(atob(parts[1]));

		// The signature (third part) remains encoded
		const signature = parts[2];

		return {
			header,
			payload,
			signature,
			raw: {
				header: parts[0],
				payload: parts[1],
				signature: parts[2]
			}
		};
	} catch (error) {
		throw new Error(`Failed to decode JWT: ${error.message}`);
	}
}
