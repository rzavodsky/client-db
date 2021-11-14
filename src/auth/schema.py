from jsonschema import Draft7Validator

# All routes that require auth
perm_routes = ["client", "contact", "auth"]

auth_schema = {
    "type": "object",
    "properties": {
        "permissions": {
            "type": "object",
            "properties": { perm: { "type": "integer", "minimum": 0, "maximum": 100 } for perm in perm_routes},
            "additionalProperties": False,
        }
    },
    "additionalProperties": False,
    "required": ["permissions"]
}

Draft7Validator.check_schema(auth_schema)

AuthValidator = Draft7Validator(auth_schema)
