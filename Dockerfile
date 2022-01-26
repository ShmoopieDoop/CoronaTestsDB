FROM python:3.10-slim
ARG PORT=5000
ENV PORT=$PORT
EXPOSE $PORT
COPY requirements.txt .
RUN pip install -r requirements.txt
ARG MONGO_USER_PASSWORD
WORKDIR /app
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app