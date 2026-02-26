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

overseer.register_template({
  name = "auth",
  builder = function()
    return {
      cmd = "uv run fastapi dev --port 8001 src/auth/main.py",
      cwd = vim.fs.joinpath(vim.fn.getcwd(), "services", "auth"),
      components = { "default", "unique" }
    }
  end,
})
