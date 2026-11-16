FROM python:3.11-alpine

# Create secure non-root user
RUN adduser -D -u 10001 appuser

WORKDIR /app

# Ensure pip, setuptools, wheel are upgraded to patched versions
RUN pip install --no-cache-dir --upgrade pip setuptools wheel jaraco.context

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN chown -R appuser:appuser /app

USER appuser

ENV PORT=5000 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
