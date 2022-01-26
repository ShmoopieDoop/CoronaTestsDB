import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import find_location
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


class Locations(Resource):
    def post(self):
        args = location_get_args.parse_args()
        point = args["point"]
        count = args["locCount"]
        locs = find_location.find_near(point, count)
        return locs, 201, {"Access-Control-Allow-Origin": "*"}


class Refresh(Resource):
    def post(self):
        return {"stuff": "Hello World"}


api.add_resource(Locations, "/locations")
api.add_resource(Refresh, "/refresh")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("API_PORT"), debug=True)
