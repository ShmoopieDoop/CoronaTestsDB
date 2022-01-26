FROM python:latest
RUN pip install flask "pymongo[srv]"  requests  flask-restful flask-cors beautifulsoup4 python-dotenv
ARG MONGO_USER_PASSWORD
WORKDIR /app
COPY . .
ENTRYPOINT [ "python3", "api.py" ]