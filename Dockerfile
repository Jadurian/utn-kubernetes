FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY etl_script.py /app/

CMD ["python3"]

ENTRYPOINT ["app/etl_script.py"]

