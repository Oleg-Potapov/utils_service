from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
RATES_URL = os.environ.get('RATES_URL')
WSDL = os.environ.get('WSDL')
BITCOIN_URL = os.environ.get('BITCOIN_URL')
CBR_URL = os.environ.get('CBR_URL')
