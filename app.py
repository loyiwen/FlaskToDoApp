from flask import Flask
from models import db
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialise SQLAlchemy with app
db.init_app(app)

@app.route('/')
def index():
    return "Home Page Text"

@app.route('/create')
def create():
    return "Create Assessment Page Text"

if __name__ == '__main__':
    app.run(debug=True)
