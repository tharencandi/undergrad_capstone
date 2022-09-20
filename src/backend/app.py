from flask import Flask, request, jsonify


app = Flask(__name__)

@app.get('/')
def index():
    return jsonify("hello world")




if __name__ == '__main__':
	app.run(debug=True)

