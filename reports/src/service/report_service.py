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
    def fetch_incidents(self, token_encabezado, canal_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None, tipo_id=None):
        try:
            url = f"{INCIDENT_URL}summary"
            headers = {"Authorization": token_encabezado}
            params = {
                "canal_id": canal_id,
                "estado_id": estado_id,
                "tipo_id": tipo_id,
                "fecha_inicio": fecha_inicio.strftime('%m/%d/%Y') if fecha_inicio else None,
                "fecha_fin": fecha_fin.strftime('%m/%d/%Y') if fecha_fin else None
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            incidents_data = response.json()
            return incidents_data['incidentes'] if 'incidentes' in incidents_data else []

        except requests.RequestException as e:
            logging.error(f"Error al obtener los incidentes desde {url}: {e}")
            raise ServerSystemException("No se pudo obtener los datos de los incidentes. Por favor, contacte al administrador.")
        
    def save_report(self, nombre_reporte, incidentes, estado_id=None, tipo_id=None, canal_id=None, fecha_inicio=None, fecha_fin=None):
        try:
            nuevo_reporte = Report(
                nombre_reporte=nombre_reporte,
                estado_id=estado_id,
                tipo_id=tipo_id,
                canal_id=canal_id,
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

    def generate_pdf_report(self, nombre_reporte, incidentes):
        from weasyprint import HTML
        from jinja2 import Environment, FileSystemLoader, Template

        try:
            template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
            env = Environment(loader=FileSystemLoader(template_dir))

            logo_path = os.path.join(template_dir, 'logo.png')

            template = env.get_template("template_es.html")

            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../generated_reports'))
            os.makedirs(output_dir, exist_ok=True)

            pdf_file = os.path.join(output_dir, f"{nombre_reporte}.pdf")

            rendered_html = template.render(nombre_reporte=nombre_reporte, incidentes=incidentes, logo_path=logo_path)

            HTML(string=rendered_html).write_pdf(pdf_file)

            return pdf_file

        except Exception as e:
            logging.error(f"Error al generar el PDF: {e}")
            raise ServerSystemException("No se pudo generar el PDF del reporte. Por favor, contacte al administrador.")
