from flask import jsonify
from sqlalchemy import func
from ..models.models import Incidente, IncidenteSchema, Canal, db
from ..utils.utils import CommonUtils
from ..errors.errors import ServerSystemException
from dotenv import load_dotenv
import random, logging, os

incident_schema = IncidenteSchema()
common_utils = CommonUtils()

load_dotenv('.env.template')
USER_URL = os.environ.get('USER_PATH')

class BoardService():
    def get_percentage_by_channel(self, canal_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None):
        query = db.session.query(
            Canal.nombre_canal.label("canal"),
            func.count(Incidente.id).label("total")
        ).join(Canal, Incidente.canal_id == Canal.id)
    
        if canal_id:
            query = query.filter(Incidente.canal_id == canal_id)
        if estado_id:
            query = query.filter(Incidente.estado_id == estado_id)
        if fecha_inicio and fecha_fin:
            query = query.filter(Incidente.fecha_creacion.between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            query = query.filter(Incidente.fecha_creacion >= fecha_inicio)
        elif fecha_fin:
            query = query.filter(Incidente.fecha_actualizacion <= fecha_fin)
    
        total_incidents = query.with_entities(func.count(Incidente.id)).scalar() or 1
    
        results = query.group_by(Canal.nombre_canal).all()
    
        percentages = {
            canal: round((total / total_incidents) * 100) for canal, total in results
        }
        
        return percentages
    
    def get_summarized_incidents(self, canal_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None):        
        query = db.session.query(
            Incidente.id,
            Incidente.codigo,
            Incidente.asunto,
            Incidente.fecha_creacion,
            Incidente.fecha_actualizacion,
            Incidente.canal_id,
            Incidente.estado_id,
            Incidente.tipo_id
        )
        
        if canal_id:
            query = query.filter(Incidente.canal_id == canal_id)
        if estado_id:
            query = query.filter(Incidente.estado_id == estado_id)
        if fecha_inicio and fecha_fin:
            query = query.filter(Incidente.fecha_creacion.between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            query = query.filter(Incidente.fecha_creacion >= fecha_inicio)
        elif fecha_fin:
            query = query.filter(Incidente.fecha_actualizacion <= fecha_fin)
        
        incidentes = query.all()
        
        resultado = [
            {
                "id": incidente.id,
                "codigo": incidente.codigo,
                "asunto": incidente.asunto,
                "fecha_creacion": incidente.fecha_creacion,
                "fecha_actualizacion": incidente.fecha_actualizacion,
                "canal_id": incidente.canal_id,
                "estado_id": incidente.estado_id,
                "tipo_id": incidente.tipo_id
            }
            for incidente in incidentes
        ]
        
        return jsonify(incidentes=resultado, total=len(resultado))
    