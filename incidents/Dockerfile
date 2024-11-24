FROM python:3.9

WORKDIR /app

COPY Pipfile* ./

#COPY experimentos-435400-a8c250104b8f.json /app/experimentos-435400-a8c250104b8f.json

RUN pip install pipenv && pipenv install --ignore-pipfile

COPY . .

#ENV GOOGLE_APPLICATION_CREDENTIALS="/app/experimentos-435400-a8c250104b8f.json"

ENV FLASK_APP=src/main.py

EXPOSE 3004

CMD ["pipenv", "run","python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3004"] 