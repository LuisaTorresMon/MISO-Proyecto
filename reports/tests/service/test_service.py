from datetime import datetime
from unittest.mock import MagicMock
import pytest
from faker import Faker
import requests
from src.errors.errors import ServerSystemException
from src.main import app
from src.service.report_service import INCIDENT_URL, ReportService

fake = Faker()       
report_service = ReportService()

class TestService():
    @pytest.fixture
    def report_service(self, mocker):
        return ReportService()

    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client

    def test_fetch_incidents_success(self, report_service, mocker):
        mock_response_data = {
            "incidentes": [
                {
                    "asunto": "incidente_llamada",
                    "canal": "Llamada Telefónica",
                    "codigo": "INC01565",
                    "estado": "Abierto",
                    "fecha_actualizacion": "11/15/2024",
                    "fecha_creacion": "11/15/2024",
                    "id": 5,
                    "tipo": "Petición"
                },
                {
                    "asunto": "internet",
                    "canal": "Correo Electrónico",
                    "codigo": "INC01235",
                    "estado": "Abierto",
                    "fecha_actualizacion": "11/15/2024",
                    "fecha_creacion": "11/15/2024",
                    "id": 7,
                    "tipo": "Queja/Reclamo"
                },
            ],
            "total": 8
        }

        mock_get = mocker.patch('requests.get')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        token = "Bearer test-token"
        result = report_service.fetch_incidents(token_encabezado=token, canal_id=1, estado_id=2, tipo_id=3,
                                                fecha_inicio=datetime(2024, 11, 15), fecha_fin=datetime(2024, 11, 16))

        assert result == mock_response_data['incidentes']
        mock_get.assert_called_once_with(
            f"{INCIDENT_URL}summary",
            params={
                "canal_id": 1,
                "estado_id": 2,
                "tipo_id": 3,
                "fecha_inicio": "11/15/2024",
                "fecha_fin": "11/16/2024"
            },
            headers={"Authorization": token}
        )

    def test_fetch_incidents_failure(self, report_service, mocker):
        mock_get = mocker.patch('requests.get')
        mock_get.side_effect = requests.RequestException("Connection Error")

        with pytest.raises(ServerSystemException, match="No se pudo obtener los datos de los incidentes. Por favor, contacte al administrador."):
            report_service.fetch_incidents(token_encabezado="Bearer test-token")
    
    def test_save_report_success(self, report_service, mocker):
        mock_db_session = mocker.patch('src.models.model.db.session')
        
        report_instance = MagicMock(id=123)
        mocker.patch('src.service.report_service.Report', return_value=report_instance)

        result = report_service.save_report(
            nombre_reporte="Reporte Test",
            incidentes=[{"id": 1}, {"id": 2}],
            estado_id=1, tipo_id=2, canal_id=3, 
            fecha_inicio=datetime(2023, 1, 1), fecha_fin=datetime(2023, 1, 31)
        )

        assert result == report_instance
        mock_db_session.add.assert_called_once_with(report_instance)
        mock_db_session.commit.assert_called_once()
    
    def test_save_report_failure(self, report_service, mocker):
        mock_db_session = mocker.patch('src.models.model.db.session')
        mock_db_session.commit.side_effect = Exception("DB Error")

        with pytest.raises(ServerSystemException, match="No se pudo guardar el reporte. Por favor, contacte al administrador."):
            report_service.save_report(nombre_reporte="Reporte Fallido", incidentes=[])
    
    def test_generate_pdf_report_success(self, mocker, report_service, tmp_path):
        mock_weasyprint = MagicMock()
        mock_html = MagicMock()
        mock_weasyprint.HTML = mock_html
        mocker.patch.dict('sys.modules', {'weasyprint': mock_weasyprint})

        mock_instance = mock_html.return_value
        mock_instance.write_pdf = MagicMock()

        mock_env = mocker.patch('jinja2.Environment')
        mock_env.return_value.get_template.return_value.render.return_value = "<html>Rendered HTML</html>"

        mocker.patch('os.path.abspath', side_effect=lambda x: str(tmp_path / x))
        mocker.patch('os.makedirs')

        pdf_file = report_service.generate_pdf_report(nombre_reporte="ReportePDF", incidentes=[{"id": 1}, {"id": 2}])

        assert pdf_file.endswith("ReportePDF.pdf")

        mock_html.assert_called_once_with(string="<html>Rendered HTML</html>")
        mock_instance.write_pdf.assert_called_once_with(pdf_file)
    
    def test_generate_pdf_report_failure(self, report_service, mocker):
        mock_weasyprint = MagicMock()
        mock_html = MagicMock()
        mock_weasyprint.HTML = mock_html
        mocker.patch.dict('sys.modules', {'weasyprint': mock_weasyprint})

        mock_instance = mock_html.return_value
        mock_instance.write_pdf = MagicMock()

        mock_env = mocker.patch('jinja2.Environment')
        mock_env.side_effect = Exception("Template Error")

        with pytest.raises(ServerSystemException, match="No se pudo generar el PDF del reporte. Por favor, contacte al administrador."):
            report_service.generate_pdf_report(nombre_reporte="Reporte Fallido", incidentes=[])
