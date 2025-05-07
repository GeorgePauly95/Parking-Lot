from flask import Flask
from src.controller import register_routes

app = Flask(__name__)
register_routes(app)

@app.route('/')
def home():
    return '<title>BbB Parking Lot!</title> <h1>BbB Parking Lot!</h1>', 200, {"Access-Control-Allow-Origin":"*"}

if __name__ == "__main__":
    app.run(debug=True)