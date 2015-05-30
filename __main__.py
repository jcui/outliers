import argparse
from flask_app import flask_app

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()
flask_app.run(args.debug)
