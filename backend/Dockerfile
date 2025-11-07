# build stage
FROM python:3.13 AS builder

WORKDIR /app
ENV PYTHONPATH=/app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# runtime stage
FROM python:3.13-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app /app/app
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
