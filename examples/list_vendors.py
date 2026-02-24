import os
import sys
from alignbooks import AlignBooks

def get_client():
    return AlignBooks(
        email=os.environ.get("AB_EMAIL", "test@example.com"),
        password=os.environ.get("AB_PASSWORD", "test"),
        api_key=os.environ.get("AB_API_KEY", "test"),
        enterprise_id=os.environ.get("AB_ENTERPRISE_ID", "test"),
        company_id=os.environ.get("AB_COMPANY_ID", "test"),
        user_id=os.environ.get("AB_USER_ID", "test")
    )

if __name__ == "__main__":
    ab = get_client()
    vendors = ab.vendors.list()
    print(f"Found {len(vendors)} vendors.")
