from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MICROSERVICES = {
    'incident': 'http://localhost:3004',
    'invoice': 'http://localhost:3002',
    'payment': 'http://localhost:3001',
    'plan': 'http://localhost:3003',
    'user': 'http://localhost:3000'
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service, path):
    if service in MICROSERVICES:
        service_url = f"{MICROSERVICES[service]}/{service}/{path}"

        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']  # Captura el encabezado de autorización
            headers['Technology'] = request.headers['Technology']

        try:
            if request.method == 'GET':
                response = requests.get(service_url, params=request.args, headers=headers)
            elif request.method == 'POST':
                if request.content_type.startswith('multipart/form-data'):
                    response = requests.post(service_url, data=request.form, files=request.files, headers=headers)
                else:
                    response = requests.post(service_url, json=request.json, headers=headers)
            elif request.method == 'PUT':
                response = requests.put(service_url, json=request.json, headers=headers)
            elif request.method == 'DELETE':
                response = requests.delete(service_url, headers=headers)

            # Devolver la respuesta del microservicio
            return jsonify(response.json()), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to connect to service"}), 503
    else:
        return jsonify({"error": "Service not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)