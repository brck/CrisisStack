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




