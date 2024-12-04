FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir requests psycopg2-binary

COPY etl_script.py .

CMD ["python", "etl_script.py"]

# ENTRYPOINT ["etl_script.py"]

