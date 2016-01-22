local schema = require("lapis.db.schema")

local types = schema.types

schema.create_table("applciations", {
  {"id", types.serial({ primary_key = true, null = false })},
  {"name", types.varchar({null = false})},
  {"version",types.double({null = false})},
  {"description",types.text({null = false})},
  {"size",types.double({null = false})},
  {"OsVersion",types.double({null = false})},
  {"downloads",types.integer({null = false})},
  {"launchURL",types.varchar({null = false})},
  {"checksum", types.serial({null = false})},
  {"permissions", types.varchar({array = true, null = false})}
  "PRIMARY KEY (id)"
})

schema.create_table("address",{
  {"id",types.serial({ primary_key = true, null = false })},
  {"email",types.varchar({null=false}), 
  {"developerid",types.foreign_key({null = false})}
})

schema.create_table("developerinformation",{
    {"id", types.serial({ primary_key = true, null = false })},
    {"name", types.varchar({null = false})},
    {"website",types.varchar({null = true })},
    {"email",types.varchar({null= false})}
	})

schame.create_table("applciationcategory",{
   {"id", types.serial({ primary_key = true, null = false })},
   {"name", types.varchar({primary_key = true , null = false })}
	})

schema.create_table("applciationupdate",{
    {"id", types.serial({ primary_key = true, null = false })},
    {"applciationid",types.foreign_key({ null= false}), 
    {"version",types.integer({null=false})},
    {"updateinformation",types.varchar({null=false})}
    })	