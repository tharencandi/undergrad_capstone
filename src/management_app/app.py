
from flask import Flask
import logging

logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__)

@app.post("/<string:case>/<uuid>/svs")
def receive_svs(case, uuid):
    print("svs")

@app.post("/<string:case>/<uuid>/mask")
def receive_mask(case, uuid):
    print("mask")

@app.post("/<string:case>/<uuid>/annotation")
def receive_annotation(case, uuid):
    print("annotation")

if __name__=="__main__":
    app.run(host="0.0.0.0")
