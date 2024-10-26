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

        try:
            if request.method == 'GET':
                response = requests.get(service_url, params=request.args)
            elif request.method == 'POST':
                response = requests.post(service_url, json=request.json)
            elif request.method == 'PUT':
                response = requests.put(service_url, json=request.json)
            elif request.method == 'DELETE':
                response = requests.delete(service_url)

            # Devolver la respuesta del microservicio
            return jsonify(response.json()), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to connect to service"}), 503
    else:
        return jsonify({"error": "Service not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)