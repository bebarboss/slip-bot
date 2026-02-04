FROM python:3.11-slim

# Install system dependencies (Tesseract + runtime libs for OpenCV)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-tha \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Run the app (module: app.main, app object: app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]