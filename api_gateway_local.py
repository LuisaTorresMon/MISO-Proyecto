from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import logging

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers=["Authorization", "Technology"])

MICROSERVICES = {
    'incident': 'http://localhost:3004',
    'invoice': 'http://localhost:3002',
    'payment': 'http://localhost:3001',
    'plan': 'http://localhost:3003',
    'user': 'http://localhost:3000',
    'report': 'http://localhost:3006',
    'ia': 'http://localhost:3005',
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service, path):
    if service in MICROSERVICES:
        service_url = f"{MICROSERVICES[service]}/{service}/{path}"

        headers = {}
        if 'Authorization' in request.headers:
            headers['Authorization'] = request.headers['Authorization']
            headers['Technology'] = request.headers['Technology']

        try:
            if request.method == 'GET':
                response = requests.get(service_url, params=request.args, headers=headers)
            elif request.method == 'POST':
                if request.content_type.startswith('multipart/form-data'):
                    files = [('files', (file.filename, file.stream, file.mimetype)) for file in request.files.getlist('files')]
                    response = requests.post(service_url, data=request.form, files=files, headers=headers, timeout=10000)
                else:
                    response = requests.post(service_url, json=request.json, headers=headers)
            elif request.method == 'PUT':
                response = requests.put(service_url, json=request.json, headers=headers)
            elif request.method == 'DELETE':
                response = requests.delete(service_url, headers=headers)

            return jsonify(response.json()), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to connect to service"}), 503
    else:
        return jsonify({"error": "Service not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)