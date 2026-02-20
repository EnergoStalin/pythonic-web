(async function() {
	const config = await fetch(AUTH_CONFIG_ENDPOINT).then(e => e.json());

	const v = config.validation

	fio_description.textContent = v.fio.description
	fio.pattern = v.fio.regex
	password_description.textContent = v.password.description
	password.pattern = v.password.regex
})()
