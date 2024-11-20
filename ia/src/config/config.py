from flask import Flask
from dotenv import load_dotenv

class Config:

    @staticmethod
    def init():
        app = Flask(__name__) 
        
        load_dotenv('.env.template')
      
        app_context = app.app_context()
        app_context.push()

        return app