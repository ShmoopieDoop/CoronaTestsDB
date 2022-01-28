FROM python:3.10-slim
RUN apt-get update
RUN apt-get install cron -y 

# # Add crontab file in the cron directory
# # RUN echo "* * * * * python /app/insert_to_db.py" > /etc/cron.d/refresh-data
# RUN echo "* * * * * /usr/local/bin/python /app/insert_to_db.py > /app/insert_to_db.log" > /etc/cron.d/refresh-data

# # Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/refresh-data
# RUN crontab /etc/cron.d/refresh-data

ARG PORT=5000
ENV PORT=$PORT
EXPOSE $PORT
COPY requirements.txt .
RUN pip install -r requirements.txt
ARG MONGO_USER_PASSWORD
WORKDIR /app
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app