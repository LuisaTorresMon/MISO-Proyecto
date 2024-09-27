FROM python:3.9

WORKDIR /app

COPY Pipfile* ./

# COPY experimentos-435400-9400b9b6b125.json /app/experimentos-435400-9400b9b6b125.json

RUN pip install pipenv && pipenv install --ignore-pipfile

COPY . .

# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/experimentos-435400-9400b9b6b125.json"

ENV FLASK_APP=src/main.py

EXPOSE 3002

CMD ["pipenv", "run","python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3004"]