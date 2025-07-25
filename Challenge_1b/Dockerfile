FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY challenge1b.py .

RUN pip install --no-cache-dir PyMuPDF

CMD ["python", "challenge1b.py"]
