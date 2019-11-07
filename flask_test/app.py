from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #__name__ references this file.
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    completed=db.Column(db.Integer, default=0)
    date_created=db.Column(db.DateTime, default=datetime.utcnow) #Uses the default to set it to the current time.

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST': #If it's a POST request... then
        pass
    else:
        return render_template('index.html') #You don't have to specify folder name because it knows to look for a folder called 'templates'

if __name__ == "__main__":
    app.run(debug=True)