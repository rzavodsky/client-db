import secrets

def generate_key():
    """Generates a new 32-byte token"""
    return secrets.token_urlsafe(32)
