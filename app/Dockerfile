FROM python:3.11-alpine

# Apply all Alpine OS security upgrades
RUN apk update && apk upgrade --no-cache

# Create secure non-root user
RUN adduser -D -u 10001 appuser

WORKDIR /app

# Install application dependencies and strip build tooling to achieve ZERO vulnerabilities
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel pip \
    && rm -rf /root/.cache

COPY app.py .
RUN chown -R appuser:appuser /app

USER appuser

ENV PORT=5000 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
