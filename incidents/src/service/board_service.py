from flask import jsonify
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import dialect
from ..models.models import Estado, Incidente, IncidenteSchema, Canal, Tipo, db
from ..utils.utils import CommonUtils
from ..errors.errors import ServerSystemException
from dotenv import load_dotenv
import random, logging, os
from datetime import datetime
import logging

incident_schema = IncidenteSchema()
common_utils = CommonUtils()

load_dotenv('.env.template')
USER_URL = os.environ.get('USER_PATH')

class BoardService():
    def get_percentage_by_channel(self, canal_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None):
        base_query = db.session.query(
            func.count(Incidente.id).label("total")
        )

        if fecha_inicio:
            fecha_inicio = fecha_inicio.date()

        if fecha_fin:
            fecha_fin = fecha_fin.date()

        if estado_id:
            base_query = base_query.filter(Incidente.estado_id == estado_id)
        if fecha_inicio and fecha_fin:
            base_query = base_query.filter(func.date(Incidente.fecha_creacion).between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            base_query = base_query.filter(func.date(Incidente.fecha_creacion) >= fecha_inicio)
        elif fecha_fin:
            base_query = base_query.filter(func.date(Incidente.fecha_creacion) <= fecha_fin)

        total_incidents = base_query.scalar() or 1

        query = db.session.query(
            Canal.nombre_canal.label("canal"),
            func.count(Incidente.id).label("total")
        ).join(Canal, Incidente.canal_id == Canal.id)


    
        if canal_id:
            query = query.filter(Incidente.canal_id == canal_id)
        if estado_id:
            query = query.filter(Incidente.estado_id == estado_id)
        if fecha_inicio and fecha_fin:
            query = query.filter(func.date(Incidente.fecha_creacion).between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            query = query.filter(func.date(Incidente.fecha_creacion) >= fecha_inicio)
        elif fecha_fin:
            query = query.filter(func.date(Incidente.fecha_creacion) <= fecha_fin)
    
        results = query.group_by(Canal.nombre_canal).all()

        percentages = {
            canal: round((total / total_incidents) * 100) for canal, total in results
        }

        key_value_array = [{"channel": canal, "value": percentage} for canal, percentage in percentages.items()]

        return jsonify(channels=key_value_array)
    
    def get_summarized_incidents(self, canal_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None, tipo_id=None):        
        query = db.session.query(
            Incidente.id,
            Incidente.codigo,
            Incidente.asunto,
            Incidente.fecha_creacion,
            Incidente.fecha_actualizacion,
            Canal.nombre_canal.label('nombre_canal'),
            Estado.estado.label('estado'),
            Tipo.tipo.label('tipo')
        ).join(Canal, Incidente.canal_id == Canal.id) \
        .join(Estado, Incidente.estado_id == Estado.id) \
        .join(Tipo, Incidente.tipo_id == Tipo.id)

        if fecha_inicio:
            fecha_inicio = fecha_inicio.date()

        if fecha_fin:
            fecha_fin = fecha_fin.date()

        if canal_id:
            query = query.filter(Incidente.canal_id == canal_id)
        if estado_id:
            query = query.filter(Incidente.estado_id == estado_id)
        if tipo_id:
            query = query.filter(Incidente.tipo_id == tipo_id)
        if fecha_inicio and fecha_fin:
            query = query.filter(func.date(Incidente.fecha_creacion).between(fecha_inicio, fecha_fin))
        elif fecha_inicio:
            query = query.filter(func.date(Incidente.fecha_creacion) >= fecha_inicio)
        elif fecha_fin:
            query = query.filter(func.date(Incidente.fecha_creacion) <= fecha_fin)
        
        incidentes = query.all()

        #compiled = query.statement.compile(dialect=dialect(), compile_kwargs={"literal_binds": True})
        #logging.debug("Summary =========>>>>>>>>> " + str(compiled))
        
        resultado = [
            {
                "id": incidente.id,
                "codigo": incidente.codigo,
                "asunto": incidente.asunto,
                "fecha_creacion": incidente.fecha_creacion.strftime('%Y-%m-%d') if incidente.fecha_creacion else None,
                "fecha_actualizacion": incidente.fecha_creacion.strftime('%Y-%m-%d') if incidente.fecha_creacion else None,
                "canal": incidente.nombre_canal,
                "estado": incidente.estado,
                "tipo": incidente.tipo
            }
            for incidente in incidentes
        ]
        
        return jsonify(incidentes=resultado, total=len(resultado))
    
    