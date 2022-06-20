from email.policy import default
from flask import Flask, render_template, request, redirect
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

@app.route("/", methods=["GET","POST"])
def hello_world():

    if request.method == 'POST':
        visitor_log = visitor_list(email_id=request.form["email"], name=request.form['name'],company=request.form['company'])
        db.session.add(visitor_log)
        db.session.commit()

    # #whenever the page loads this gets logged in the database
    # visitor_log = visitor_list(email_id="xyz@lol.com", name="random",company="abc")
    # db.session.add(visitor_log)
    # db.session.commit()

    #Querying all the records
    all_visitors = visitor_list.query.all()
    return render_template('index.html',all_visitors=all_visitors)
    #return "<p>Hello, World!</p>"

@app.route("/show")
def products():
    all_visitors = visitor_list.query.all()
    print(all_visitors)
    return "<p>This is the product page</p>"

@app.route("/delete/<int:sno>")
def delete_row(sno):
    visitor = visitor_list.query.filter_by(sno=sno).first()
    db.session.delete(visitor)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET","POST"])
def update_row(sno):
    if request.method == 'POST':
        visitor = visitor_list.query.filter_by(sno=sno).first()
        visitor.email_id=request.form["email"]
        visitor.name=request.form['name']
        visitor.company=request.form['company']
        #db.session.add(visitor)
        db.session.commit()

        return redirect('/')

    else:
        visitor = visitor_list.query.filter_by(sno=sno).first()
    
    return render_template('update.html', visitor=visitor)

@app.route("/about")
def about():
   
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)