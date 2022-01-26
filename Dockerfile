FROM python:latest
ARG PORT=5000
ENV PORT=$PORT
EXPOSE $PORT
COPY requirements.txt .
RUN pip install -r requirements.txt
ARG MONGO_USER_PASSWORD
WORKDIR /app
COPY . .
ENTRYPOINT [ "python3", "api.py" ]