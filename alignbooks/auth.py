"""Authentication utilities for AlignBooks API.

Handles AES-256-CBC encryption for ab_token generation and login response decryption.
"""

from __future__ import annotations

import base64
import json
import os
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from .constants import (
    AES_IV_ZERO,
    AES_KEY,
    DEFAULT_MASTER_TYPE,
    PBKDF2_ITERATIONS,
    PBKDF2_KEY_LENGTH,
)


def make_ab_token(
    api_key: str,
    enterprise_id: str,
    company_id: str,
    user_id: str,
    username: str,
    password: str,
    apiname: str,
    master_type: int = DEFAULT_MASTER_TYPE,
) -> str:
    """Generate an encrypted ab_token header value.

    The token is a PBKDF2+AES-256-CBC encrypted JSON containing all auth fields.
    Format: Base64(salt[16] + iv[16] + ciphertext)

    Args:
        api_key: AlignBooks API key (GUID).
        enterprise_id: Enterprise ID (GUID).
        company_id: Company ID (GUID).
        user_id: User ID (GUID).
        username: Login email.
        password: Login password.
        apiname: The API endpoint name being called.
        master_type: Master type code (default 2037).

    Returns:
        Base64-encoded encrypted token string.
    """
    header_info = {
        "username": username,
        "password": password,
        "enterprise_id": enterprise_id,
        "company_id": company_id,
        "user_id": user_id,
        "apiname": apiname,
        "apikey": api_key,
        "master_type": master_type,
        "client_date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    plaintext = json.dumps(header_info).encode("utf-8")
    salt = os.urandom(16)
    key = PBKDF2(AES_KEY, salt, dkLen=PBKDF2_KEY_LENGTH, count=PBKDF2_ITERATIONS)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return base64.b64encode(salt + iv + ciphertext).decode("utf-8")


def decrypt_login_response(encrypted_b64: str) -> dict:
    """Decrypt an AES-256-CBC encrypted login response.

    Used when authenticating with individual headers (legacy method).
    The ab_token method returns plain JSON, so decryption is not needed.

    Args:
        encrypted_b64: Base64-encoded encrypted JSON string.

    Returns:
        Decrypted session data as a dictionary.
    """
    encrypted = base64.b64decode(encrypted_b64)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=AES_IV_ZERO)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size).decode("utf-8")
    return json.loads(decrypted)
