
from codecs import register
from flask import Flask,render_template ,url_for,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.secret_key = "my secret key"

db =SQLAlchemy(app)

class students(db.Model):
     id = db.Column('student_id', db.Integer, primary_key = True)
     name = db.Column(db.String(100))
     contacts = db.Column(db.String(10))
     address= db.Column(db.String(200)) 
     code = db.Column(db.String(4))

     def __init__(self, name, contacts, address,code):
          self.name = name
          self.contacts = contacts
          self.address = address
          self.code = code



@app.route('/')
def show_all():
     return render_template('show_all.html', students = students.query.all() )



@app.route('/new', methods = ['GET', 'POST'])
def new():
     if request.method == 'POST':
          if not request.form['name'] or not request.form['contacts'] or not request.form['address'] or not request.form['code']:
               flash('Please enter all the fields', 'error')
          else:
               student = students(request.form['name'], request.form['contacts'],request.form['address'], request.form['code'])
          db.session.add(student)
          db.session.commit()
          flash('Record was successfully added')
          return redirect('/')
     return render_template('new.html')




@app.route('/delete/<int:id>')
def stud_delete(id):
     stud= students.query.get(id)
     try:

          db.session.delete(stud)
          db.session.commit()
          flash('Record was successfully deleted')
          return redirect('/')
     except:
          return "The was a problem deleting the record"




@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
     stud = students.query.get(id)
     if request.method == 'POST':
          stud.name = request.form['name']
          stud.contacts =request.form['contacts']
          stud.address = request.form['address']
          stud.code = request.form['code']

          try:
               db.session.commit()
               return redirect('/')
          except:
               return "The was a problem updating the  details"

     else:
          return render_template('update.html',stud=stud)





if __name__ == '__main__':
     db.create_all()
     app.run(debug = True)