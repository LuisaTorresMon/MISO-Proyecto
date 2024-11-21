from src.main import app

class TestBlueprints:

    def test_ping(self):
        with app.test_client() as test_client:
            response = test_client.get('/ia/ping')
            assert response.data.decode("utf-8") == "pong", response

    def test_online(self, mocker):
        mock_prediction = {"prediction": "Prediction"}
        mocker.patch(
            'src.utils.utils.CommonUtils.get_ia_prediction',  # Ruta completa al método
            return_value=mock_prediction
        )

        # Crear un cliente de pruebas de Flask
        with app.test_client() as client:
            # Datos de entrada simulados
            input_data = {"subject": "subject", "context": "some test context"}

            # Hacer la solicitud POST
            response = client.post(
                '/ia/sync',
                json=input_data  # Enviar datos como JSON
            )

            # Validar la respuesta
            assert response.status_code == 200
            response_data = response.get_json()
            assert response_data == {"prediction": mock_prediction}
