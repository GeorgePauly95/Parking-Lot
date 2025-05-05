from flask import Flask
from src.controller import register_routes

app = Flask(__name__)
register_routes(app)

@app.route('/')
def home():
    return 'BbB Parking Lot!'

if __name__ == "__main__":
    app.run(debug=True)