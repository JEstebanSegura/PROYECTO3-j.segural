from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = "tu_clave_secreta_segura"