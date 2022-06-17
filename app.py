from email.policy import default
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///prediction.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class visitor_list(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    email_id = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    company = db.Column(db.String(200), nullable = False)
    logged_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route("/")
def hello_world():
    return render_template('index.html')
    #return "<p>Hello, World!</p>"

@app.route("/products")
def products():
    return "<p>This is the product page</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)