FROM python:3.10-slim
COPY  . /code
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt


ENV FLASK_APP "run.py"
ENV FLASK_ENV "development"
CMD flask run -h 0.0.0.0 -p 80



