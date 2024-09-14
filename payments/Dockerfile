FROM python:3.9

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv && pipenv install --ignore-pipfile

COPY . .

ENV FLASK_APP=src/main.py

EXPOSE 3001

CMD ["pipenv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=3001"]