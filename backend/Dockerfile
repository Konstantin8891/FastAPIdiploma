FROM python:3.10-slim
WORKDIR /app/
COPY backend/ .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
