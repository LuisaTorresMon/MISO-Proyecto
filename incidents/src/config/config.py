from flask import Flask
from ..models.models import db, cargar_datos_iniciales
from dotenv import load_dotenv
from os import environ
import logging

class Config:

    @staticmethod
    def init():
        app = Flask(__name__) 
        
        load_dotenv('.env.template')       
            
        db_url = environ.get('SQLALCHEMY_DATABASE_URI')

        app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_url}"
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
      
        app_context = app.app_context()
        app_context.push()
        
        db.init_app(app)
        db.create_all()
        
        cargar_datos_iniciales()

        return app