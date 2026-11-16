FROM python:3.11-slim

# Create secure non-root user
RUN adduser --disabled-password --gecos "" --uid 10001 appuser

WORKDIR /app

# Ensure latest system security updates are applied
RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN chown -R appuser:appuser /app

USER appuser

ENV PORT=5000 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
