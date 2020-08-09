FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./horreum /app/horreum
COPY ./etc /app/etc
COPY ./fixtures /app/fixtures

WORKDIR /app/horreum
CMD ["uvicorn", "main:app"]