FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY etl_script.py .

CMD ["python"]

ENTRYPOINT ["etl_script.py"]

