from jsonschema import Draft7Validator

client_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string", "maxLength": 50 },
        "address": { "type": "string", "maxLength": 100 },
        "ico": { "type": "string", "pattern": "^(?:(?:\d ?){8}|(?:\d ?){6})$"}, # Match a string with 6 or 8 digits, each digit can have an optional space after it
        "type": { "enum": ["pravnicka_osoba", "fyzicka_osoba"] }
    },
    "additionalProperties": False,
}
# All fields that should be required in a POST or PUT request
client_schema_required = ["name", "address", "ico", "type"]

contact_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string", "maxLength": 50 },
        "address": { "type": "string", "maxLength": 100 },
        "phone_number": { "type": "string", "pattern": "^\+?(?: ?\d){5,20}$"}, # Match a string with 5-20 digits, each digit can have a optional space before it. Can start with a +
    },
    "additionalProperties": False,
}
# All fields that should be required in a POST or PUT request
contact_schema_required = ["name", "address", "phone_number"]


Draft7Validator.check_schema({**client_schema, "required": client_schema_required})
Draft7Validator.check_schema({**contact_schema, "required": contact_schema_required})

ClientValidator = Draft7Validator({**client_schema, "required": client_schema_required}) # Used for PUT and POST requests
ClientPATCHValidator = Draft7Validator(client_schema) # Used for PATCH requests

ContactValidator = Draft7Validator({**contact_schema, "required": contact_schema_required}) # Used for PUT and POST requests
ContactPATCHValidator = Draft7Validator(contact_schema) # Used for PATCH requests