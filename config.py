import os
from dotenv import load_dotenv

load_dotenv()

private_key = os.getenv('private_key')
public_key = os.getenv('public_key')

