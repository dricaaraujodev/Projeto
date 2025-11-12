FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy server code
COPY server.py /app/server.py

# Expose ZeroMQ port (informational)
EXPOSE 5555

# Use a volume for persistence; DB will be created at /app/db.sqlite3
VOLUME ["/app"]

CMD ["python", "server.py"]
