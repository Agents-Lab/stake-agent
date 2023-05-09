import os
from cryptography.fernet import Fernet

# Generate a unique encryption key
key = Fernet.generate_key()

# Initialize the Fernet cipher suite with the generated key
cipher_suite = Fernet(key)

# Your mnemonic phrase (replace this with your actual mnemonic phrase)
mnemonic_phrase = b"Your mnemonic phrase here"

# Encrypt the mnemonic phrase
cipher_text = cipher_suite.encrypt(mnemonic_phrase)

# Print values
print(f"ENCRYPTION_KEY = {key}")
print(f"ENCRYPTED_SEED = {cipher_text}")
