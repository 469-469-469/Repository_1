import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    USERNAME = os.getenv('API_SUPERADMIN_EMAIL')
    PASSWORD = os.getenv('API_SUPERADMIN_PASSWORD')