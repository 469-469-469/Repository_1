import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    @staticmethod
    def username():
        return os.getenv("API_SUPERADMIN_EMAIL")

    @staticmethod
    def password():
        return os.getenv("API_SUPERADMIN_PASSWORD")