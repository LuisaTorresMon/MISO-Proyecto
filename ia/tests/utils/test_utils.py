import pytest
from unittest.mock import patch
from src.utils.utils import CommonUtils, IAPredictionException

class TestUtils:

    @patch("src.utils.utils.requests.post")  # Mockear la llamada a requests.post
    def test_get_ia_prediction_success(self, mock_post):
        # Configurar el mock de la respuesta
        mock_response_data = {
            "choices": [
                {"message": {"content": "Mocked assistant response"}}
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data

        # Crear una instancia de CommonUtils y llamar al método
        common_utils = CommonUtils()
        response = common_utils.get_ia_prediction("", "mocked context")

        # Verificar el resultado
        assert response == "Mocked assistant response"
        mock_post.assert_called_once()  # Asegura que requests.post fue llamado una vez

    @patch("src.utils.utils.requests.post")
    def test_get_ia_prediction_failure(self, mock_post):
        # Configurar el mock para un error en la API
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"

        common_utils = CommonUtils()

        # Verificar que se lanza una excepción en caso de error
        with pytest.raises(IAPredictionException) as excinfo:
            common_utils.get_ia_prediction("", "mocked context")

        assert "Error en la llamada a la API" in str(excinfo.value)
        mock_post.assert_called_once()

    @patch("src.utils.utils.requests.post")  # Mockear la llamada a requests.post
    def test_get_ia_prediction_with_subject(self, mock_post):
        # Configurar el mock de la respuesta
        mock_response_data = {
            "choices": [
                {"message": {"content": "Mocked assistant response with subject"}}
            ]
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data

        # Crear una instancia de CommonUtils
        common_utils = CommonUtils()

        # Llamar al método con un subject no vacío
        response = common_utils.get_ia_prediction("Test Subject", "mocked context")

        # Verificar que el contenido retornado es correcto
        assert response == "Mocked assistant response with subject"
        mock_post.assert_called_once()

    def test_obtener_token(self):
        # Crear una instancia de CommonUtils
        common_utils = CommonUtils()

        # Token de entrada
        token = "Bearer test-token-value"

        # Llamar a la función
        result = common_utils.obtener_token(token)

        # Validar que el token se procesó correctamente
        assert result == {"Authorization": "Bearer test-token-value"}, f"Resultado incorrecto: {result}"