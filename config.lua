--config.lua 
local config = require("lapis.config")

config("development", {
  port = 9090,
  greeting = "Hello mate",
  num_workers = "2",
  measure_performance = True,
  logging = {
          requests = True, 
          queries = True
}
})

config("production", {
  port = 80,
  num_workers = 4,
  code_cache = "on"
})

default_config = development