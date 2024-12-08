import hashlib
import random
import string

def generate_random_password(length=8):
    """Generate a random password of a given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def hash_password(password):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()
