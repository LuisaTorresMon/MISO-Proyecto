import pytest
import json
from unittest.mock import patch, MagicMock
from src.subscribe.subscribe_ia_request import callback, subscribe, publish_ia_response

class TestSubscribeIARequest:
    @patch('src.subscribe.subscribe_ia_request.publish_ia_response')
    @patch('src.utils.utils.CommonUtils.get_ia_prediction')  # Ruta completa al método predict_ia
    @patch('src.config.config.Config.init')
    def test_callback(self, mock_config_init, mock_predict_ia, mock_publish_ia_response):
        # Simular app y su contexto
        mock_app = MagicMock()
        mock_config_init.return_value = mock_app
        mock_app.app_context.return_value.__enter__.return_value = None

        # Simular mensaje
        message = MagicMock()
        incidence_data = {
            "incidence": {
                "id": "123",
                "asunto": "Falla en el sistema",
                "descripcion": "El sistema está caído"
            }
        }
        message.data = json.dumps(incidence_data).encode('utf-8')

        # Configurar respuesta del método predict_ia
        mock_prediction = "Predicción simulada"
        mock_predict_ia.return_value = mock_prediction

        # Llamar al callback
        callback(message)

        # Validar inicialización de la app si no existe
        mock_config_init.assert_called_once()

        # Validar que se invocó el contexto de la app
        mock_app.app_context.assert_called_once()

        # Validar llamada al método predict_ia con los argumentos correctos
        mock_predict_ia.assert_called_once_with(
            incidence_data["incidence"]["asunto"],
            incidence_data["incidence"]["descripcion"]
        )

        # Validar llamada a publish_ia_response con los argumentos correctos
        mock_publish_ia_response.assert_called_once_with(
            incidence_data["incidence"],
            mock_prediction
        )

        # Validar que el mensaje fue confirmado
        message.ack.assert_called_once()

    def test_subscribe(self, mocker):
        # Mockear el SubscriberClient y el futuro
        mock_subscriber_client = mocker.patch('google.cloud.pubsub_v1.SubscriberClient', autospec=True)
        mock_future = MockFuture()

        # Configurar el comportamiento del método `subscribe`
        mock_subscriber_instance = mock_subscriber_client.return_value
        mock_subscriber_instance.subscription_path.return_value = "mock-subscription-path"
        mock_subscriber_instance.subscribe.return_value = mock_future

        # Mockear el callback que será llamado cuando llegue un mensaje
        mocker.patch('src.subscribe.subscribe_ia_request.callback', self.mock_callback)

        # Ejecutar el código que debería disparar la suscripción
        subscribe()

        # Verifica que `subscribe` fue llamado
        mock_subscriber_instance.subscribe.assert_called_with("mock-subscription-path", callback=self.mock_callback)

        # Verifica que la suscripción realmente haya intentado ser iniciada
        assert mock_subscriber_instance.subscription_path.called

    @patch("google.cloud.pubsub_v1.PublisherClient")  # Mocking el PublisherClient
    def test_publish_ia_response(self, MockPublisherClient):
        # Crear un mock del cliente Publisher
        mock_publisher_instance = MagicMock()
        MockPublisherClient.return_value = mock_publisher_instance

        # Datos de entrada para el test
        incidence = {"id": "123"}
        context = "Predicción simulada"

        # Llamar a la función que estamos probando
        publish_ia_response(incidence, context)

        # Verificar que se haya llamado a 'publish' con el topic_name correcto y el mensaje correcto
        expected_topic_name = "projects/mock-project-id/topics/ia-prediction-topic"
        expected_message = json.dumps({
            "incidence_id": "123",
            "prediction": "Predicción simulada"
        }).encode("utf-8")
        expected_attributes = {"type": "response"}

        # Verificar que el 'publish' se haya llamado con los parámetros correctos
        mock_publisher_instance.publish.assert_called_once_with(
            expected_topic_name, expected_message, **expected_attributes
        )

        # También podríamos verificar si se ha llamado a 'future.result()' para garantizar
        # que la función trata de obtener el resultado del mensaje publicado
        mock_publisher_instance.publish.return_value.result.assert_called_once()

    def mock_callback(self, message):
        assert message.data == b'test message'


class MockFuture:
    def result(self):
        pass

    def cancel(self):
        pass