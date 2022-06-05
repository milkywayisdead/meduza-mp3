FROM python:3.8-alpine

WORKDIR /meduza_proj
COPY . .

RUN apk add -u gcc musl-dev
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000