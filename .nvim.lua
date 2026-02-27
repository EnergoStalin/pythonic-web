local overseer = require('overseer')

local cwd = vim.fn.getcwd()

overseer.register_template({
  name = "vite",
  builder = function()
    return {
      cmd = "pnpm serve",
      cwd = vim.fs.joinpath(cwd, "services", "www"),
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
  name = "api",
  builder = function()
    return {
      cmd = "uv run fastapi dev --port 8001 src/api/main.py",
      cwd = vim.fs.joinpath(cwd, "services", "api"),
      env = {
        STORAGE_POOL_PATH = vim.fs.joinpath(cwd, "data", "api", "storage", "pool"),
      },
      components = { "default", "unique" }
    }
  end,
})
