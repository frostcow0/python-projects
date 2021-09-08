from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from datetime import datetime

app = Flask(__name__,static_folder='static',template_folder='templates') #__name__ references this file.
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)
nav = Nav(app)

nav.register_element('top', Navbar(
    'nav',
    View('Lyain', 'index'),
    View('Truthan', 'index'),
))

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
        task_content=request.form['content']
        new_task=Test(content=task_content) #New Todo Object

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks=Test.query.order_by(Test.date_created).all() #Pulls all of the tasks from Todo and orders them by creation date, then sets them to variable 'task'
        return render_template('index.html', tasks=tasks) #You don't have to specify folder name because it knows to look for a folder called 'templates'

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Test.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task=Test.query.get_or_404(id)

    if request.method=='POST':
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
    #nav.init_app(app)
