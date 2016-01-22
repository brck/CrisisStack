local lapis = require("lapis")
local app = lapis.Application()
local config = require("lapis.config").get()
local respond_to = require("lapis.application").respond_to

app:get("/", function(self)
  return config.greeting .. " from port " .. config.port
end)

app:get("/MyApplications", function(self)
	return "This shall show all your applciations"
	end)

app:match("application_id","/MyApplications/:application_id", respond_to({
    GET = function(self)
	    return "This is a specific applications"
    end,
    POST = function(self)
    	--return function to go here. 
    end})) 

app:match("/MyApplications/:application_id/analytics", function(self)
	return "This is an applications analytics page "
end)

app:match("/Search", respond_to ({
    GET = function(self)
         return "This is the search page"
    end, 
    POST = function(self),
    --- return      
    end}))

app:delete("/MyApplications/:application_id/delete", function(self)
	return "delete the application"
end)

return app
