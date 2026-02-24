import unittest
from alignbooks.auth import make_ab_token

class TestAuth(unittest.TestCase):
    def test_make_token(self):
        token = make_ab_token(
            api_key="123",
            enterprise_id="123",
            company_id="123",
            user_id="123",
            username="test@test.com",
            password="pwd",
            apiname="LoginUser"
        )
        self.assertTrue(isinstance(token, str))
        self.assertTrue(len(token) > 20)

if __name__ == "__main__":
    unittest.main()
