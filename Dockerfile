FROM python:3.6.9

RUN pip install -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .
CMD ["python", "./main.py"]
