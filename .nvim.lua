local overseer = require('overseer')

overseer.register_template({
	name = "vite",
	builder = function()
		return {
			cmd = "pnpm serve",
			cwd = vim.fs.joinpath(vim.fn.getcwd(), "services", "www"),
			components = { "default", "unique" }
		}
	end,
})

overseer.register_template({
	name = "swagger",
	builder = function()
		return {
			cmd = "docker compose -f swagger-compose.yaml up -d",
			components = { "default", "unique" }
		}
	end,
})
