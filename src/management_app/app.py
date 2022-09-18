
from flask import Flask


app = Flask(__name__)

@app.post("/<string:case>/<uuid>/svs")
def receive_svs(case, uuid):
    print("svs")
    pass

@app.post("/<string:case>/<uuid>/mask")
def receive_mask(case, uuid):
    print("mask")
    pass

@app.post("/<string:case>/<uuid>/annotation")
def receive_annotation(case, uuid):
    print("annotation")
    pass

if __name__=="__main__":

    app.run()
