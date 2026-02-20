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
