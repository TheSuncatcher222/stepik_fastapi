"""
Load secrets from .env file
"""
import os

from dotenv import load_dotenv

load_dotenv()

"""Auth hash parameters"""
HASH_NAME = os.getenv('HASH_NAME')
PASS_ENCODE = os.getenv('PASS_ENCODE')
SALT = bytes(os.getenv('SALT'), encoding=PASS_ENCODE)
ITERATIONS = int(os.getenv('ITERATIONS'))

"""Encryption data"""
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_EXPIRATION_SEC = int(os.getenv('JWT_EXPIRATION_SEC'))
SECRET_KEY = os.getenv('SECRET_KEY')

"""PostgreSQL data"""
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')
