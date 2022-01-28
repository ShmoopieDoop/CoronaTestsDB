import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import find_location
import insert_to_db
import logging
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
api = Api(app)
CORS(app)

location_get_args = reqparse.RequestParser()
location_get_args.add_argument(
    "point",
    type=dict,
    help="GeoJSON object of type point must include an array with lat and long coordinates",
    required=True,
)
location_get_args.add_argument(
    "locCount",
    type=int,
    help="Number of locations to recieve sorted by shortest distance to given point",
    required=True,
)


logging.basicConfig(
    level=logging.DEBUG,
    filename="DB.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


scheduler = BackgroundScheduler()
scheduler.add_job(
    func=insert_to_db.refreshDB,
    trigger="cron",
    hour=5,
    timezone=pytz.timezone("Israel"),
)
scheduler.start()


class Locations(Resource):
    def post(self):
        args = location_get_args.parse_args()
        point = args["point"]
        count = args["locCount"]
        locs = find_location.find_near(point, count)
        return locs, 200, {"Access-Control-Allow-Origin": "*"}


class Refresh(Resource):
    def get(self):
        return {"stuff": "Hello World"}


api.add_resource(Locations, "/locations")
api.add_resource(Refresh, "/refresh")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
    atexit.register(lambda: scheduler.shutdown())
