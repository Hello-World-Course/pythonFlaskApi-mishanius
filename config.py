import os


class Config:
    # DONT EVER PUSH THIS FILE TO GIT!!!
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DEBUG = True
    OPENAI_API_KEY = ("SUPER DUPER SECRET API KEY GET IT FROM OPEN AI")
