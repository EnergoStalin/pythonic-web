export async function getToken() {
	return (await cookieStore.get("accessToken")).value
}

export async function isValid() {
	const cookie = await getToken()
}

export async function refresh() {
	return await cookieStore.get("accessToken")
}

export async function ensureSession() {
	return await cookieStore.get("accessToken")
}
