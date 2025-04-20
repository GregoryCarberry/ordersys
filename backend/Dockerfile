FROM python:3.11-slim

WORKDIR /app

# Copy all backend code EXCEPT users.db
COPY app/*.py /app/app/
COPY app/entrypoint.sh /app/
COPY requirements.txt /app/
COPY run.py /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
