FROM python:3.9-slim

WORKDIR /app

COPY ./backend/foodgram_api/requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./backend/foodgram_api/ .

CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0.0.0.0:8000" ] 
