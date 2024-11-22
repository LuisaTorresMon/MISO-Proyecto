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
    def mock_utils(self, mocker):
        mock_utils = mocker.patch('src.service.report_service.common_utils')
        return mock_utils

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

        pdf_file = report_service.generate_pdf_report(
            nombre_reporte="ReportePDF",
            incidentes=[{"id": 1}, {"id": 2}],
            lang="es"
        )

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
            report_service.generate_pdf_report(
                nombre_reporte="Reporte Fallido",
                incidentes=[],
                lang="es"
            )

    def test_obtener_token(self):
        from src.utils.utils import CommonUtils
        utils = CommonUtils()

        token = "Bearer valid_token_123"
        headers = utils.obtener_token(token)

        assert headers == {"Authorization": "Bearer valid_token_123"}

        invalid_token = "valid_token_123"
        try:
            headers = utils.obtener_token(invalid_token)
        except Exception as e:
            assert str(e) == "string index out of range"

    def test_send_email_success(self, mocker):
        from src.utils.utils import CommonUtils
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        utils = CommonUtils()

        mock_sendgrid = mocker.patch.object(SendGridAPIClient, "send", return_value=mocker.Mock(status_code=202))

        email_destination = "test@example.com"
        subject = "Test Email"
        content = "This is a test email"
        attached = None

        response = utils.send_email(email_destination, subject, content, attached)

        mock_sendgrid.assert_called_once()
        assert response["status_code"] == 202

    def test_send_email_with_attachment(self, mocker, tmp_path):
        from src.utils.utils import CommonUtils
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        utils = CommonUtils()

        mock_sendgrid = mocker.patch.object(SendGridAPIClient, "send", return_value=mocker.Mock(status_code=202))

        email_destination = "test@example.com"
        subject = "Test Email"
        content = "This is a test email"

        attachment_path = tmp_path / "test_attachment.pdf"
        with open(attachment_path, "wb") as f:
            f.write(b"This is a mock PDF content.")

        response = utils.send_email(email_destination, subject, content, str(attachment_path))

        mock_sendgrid.assert_called_once()
        assert response["status_code"] == 202

    def test_send_email_failure(self, mocker):
        from src.utils.utils import CommonUtils
        from sendgrid import SendGridAPIClient

        utils = CommonUtils()

        mocker.patch.object(SendGridAPIClient, "send", side_effect=Exception("Error sending email"))

        email_destination = "test@example.com"
        subject = "Test Email"
        content = "This is a test email"

        try:
            utils.send_email(email_destination, subject, content)
        except Exception as e:
            assert str(e) == "(500, 'Error a la hora de enviar el correo')"

    def test_send_report_pdf_by_email_success(self, report_service, mock_utils):
        mock_utils.send_email.return_value = {"status_code": 202}

        email = "test@example.com"
        name_report = "Reporte_Test"
        lang = "es"
        attached_pdf = "/path/to/report.pdf"

        response = report_service.send_report_pdf_by_email(email, name_report, lang, attached_pdf)

        assert response == {"status_code": 202}

        subject = f"Envío del reporte {name_report}" if lang == "es" else f"Sending the report {name_report}"
        content = f"Se realiza el envio automatico del reporte {name_report}, la encontrará adjunta en formato PDF" if lang == "es" else f"The report {name_report} is automatically sent, you will find it attached in PDF format"
        mock_utils.send_email.assert_called_once_with(email, subject, content, attached_pdf)
    
    def test_send_report_pdf_by_email_failure(self, report_service, mock_utils):
        mock_utils.send_email.side_effect = Exception("Error sending email")

        email = "test@example.com"
        name_report = "Reporte_Fallido"
        lang = "en"
        attached_pdf = "/path/to/report.pdf"

        with pytest.raises(Exception, match="Error sending email"):
            report_service.send_report_pdf_by_email(email, name_report, lang, attached_pdf)

        subject = f"Envío del reporte {name_report}" if lang == "es" else f"Sending the report {name_report}"
        content = f"Se realiza el envio automatico del reporte {name_report}, la encontrará adjunta en formato PDF" if lang == "es" else f"The report {name_report} is automatically sent, you will find it attached in PDF format"
        mock_utils.send_email.assert_called_once_with(email, subject, content, attached_pdf)
        