from flask import jsonify
import requests
from sqlalchemy import func
from ..models.model import db, Report, ReportSchema
from ..errors.errors import ServerSystemException
from dotenv import load_dotenv
import random, logging, os

report_schema = ReportSchema()

load_dotenv('.env.template')

USER_URL = os.environ.get('USER_PATH')
INCIDENT_URL = os.environ.get('INCIDENT_PATH')

class ReportService():
    def fetch_incidents(self, token_encabezado, canal_id=None, estado_id=None, fecha_inicio=None, fecha_final=None):
        try:
            url = f"{INCIDENT_URL}summary"
            headers = {"Authorization": token_encabezado}
            params = {
                "canal_id": canal_id,
                "estado_id": estado_id,
                "fecha_inicio": fecha_inicio.strftime('%Y-%m-%d') if fecha_inicio else None,
                "fecha_fin": fecha_final.strftime('%Y-%m-%d') if fecha_final else None
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            incidents_data = response.json()
            return incidents_data['incidentes'] if 'incidentes' in incidents_data else []

        except requests.RequestException as e:
            logging.error(f"Error al obtener los incidentes desde {url}: {e}")
            raise ServerSystemException("No se pudo obtener los datos de los incidentes. Por favor, contacte al administrador.")
        
    def save_report(self, nombre_reporte, usuario_id, incidentes, estado=None, tipo=None, canal=None, fecha_inicio=None, fecha_fin=None):
        try:
            nuevo_reporte = Report(
                nombre_reporte=nombre_reporte,
                usuario_id=usuario_id,
                estado=estado,
                tipo=tipo,
                canal=canal,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            db.session.add(nuevo_reporte)
            db.session.flush() 
            logging.debug(f"Guardando reporte {nuevo_reporte.id} con {len(incidentes)} incidentes vinculados.")

            db.session.commit()
            return nuevo_reporte

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al guardar el reporte en la base de datos: {e}")
            raise ServerSystemException("No se pudo guardar el reporte. Por favor, contacte al administrador.")
