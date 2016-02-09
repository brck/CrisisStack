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
        return {redirect_to= self:url_for('index')}
    end, 
    DELETE =function(self) 
        --do something that somewhat relates to delete. 
        return {redirect_to =self:url_for('index')}     
    end})) 

app:match("/MyApplications/:application_id/analytics", function(self)
	return "This is an applications analytics page "
end)

app:match("/Search", respond_to ({
    GET = function(self)
         return "This is the search page"
    end, 
    POST = function(self)
      --- look for that item here 
      return 'Here are your results'      
    end}))

app.default_route = function(self)
  ngx.log(ngx.NOTICE, "User hit unknown path " .. self.req.parsed_url.path)
  return lapis.Application.default_route(self)
end

app.handle_404 = function(self)
  return { status = 404, layout = false, "Not Found!" }
end


return app
