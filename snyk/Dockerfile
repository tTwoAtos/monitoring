FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 9469

CMD [ "python", "snyk.py" ]