from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Home Page Text"

@app.route('/create')
def create():
    return "Create Assessment Page Text"

if __name__ == '__main__':
    app.run(debug=True)
