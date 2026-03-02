import os
from dotenv import load_dotenv

load_dotenv()


# TODO: Load SECRET_KEY and CURRENCY_SYMBOL from environment variables using python-dotenv
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "R")

    @classmethod
    def get_currency_symbol(cls : type) -> str:
        return cls.CURRENCY_SYMBOL
    
    @classmethod
    def get_secret_key(cls : type) -> str:
        return cls.SECRET_KEY
    #com
    