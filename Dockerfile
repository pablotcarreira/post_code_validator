FROM python:3.11.6-slim

WORKDIR /usr/src/app
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 3500

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3500", "--workers", "1"]