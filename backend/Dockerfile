FROM python:3.13

WORKDIR /app
ENV PYTHONPATH=/app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
