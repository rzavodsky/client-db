from jsonschema import Draft7Validator

client_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string", "maxLength": 50 },
        "ico": { "type": "string", "maxLength": 20, "pattern": "^(?:(?:\d ?){8}|(?:\d ?){6})$"}, # Match a string with 6 or 8 digits, each digit can have an optional space after it
    },
    "additionalProperties": False,
}

# All fields that should be required in a POST or PUT request
client_schema_required = ["name", "ico"]

Draft7Validator.check_schema({**client_schema, "required": client_schema_required})

ClientValidator = Draft7Validator({**client_schema, "required": client_schema_required})
ClientPATCHValidator = Draft7Validator(client_schema)
