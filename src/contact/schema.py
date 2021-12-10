from jsonschema import Draft7Validator

contact_schema = {
    "type": "object",
    "properties": {
        "name": { "type": "string", "maxLength": 50 },
        "phone_number": { "type": "string", "pattern": "^\+?(?: ?\d){5,20}$", "maxLength": 40}, # Match a string with 5-20 digits, each digit can have a optional space before it. Can start with a +
        "email": { "type": "string", "maxLength": 100, "pattern": "^.+@.+\..+$"} # String has to include '@' and '.' in that order
    },
    "additionalProperties": False,
}

# All fields that should be required in a POST or PUT request
contact_schema_required = ["name", "phone_number", "email"]


Draft7Validator.check_schema({**contact_schema, "required": contact_schema_required})


ContactValidator = Draft7Validator({**contact_schema, "required": contact_schema_required}) # Used for PUT and POST requests
ContactPATCHValidator = Draft7Validator(contact_schema) # Used for PATCH requests
