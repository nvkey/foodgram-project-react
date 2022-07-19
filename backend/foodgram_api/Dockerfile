FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0.0.0.0:8000" ] 
