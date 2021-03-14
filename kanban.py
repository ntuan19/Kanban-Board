#import different required function 
from flask import Flask,url_for,render_template,request,redirect
#import SQLALchemy for future database creation.
from flask_sqlalchemy import SQLAlchemy

# __name__ the name of the module
app = Flask(__name__)

# /// to specify the site- relative path from the current file
#Create a file named db.sqlite later
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Create database instance- represent database as classes- intuitive.
db = SQLAlchemy(app)

#create a class Task that inherits from baseclass db.Model
class Task(db.Model):
    #use Column to define a column
    id = db.Column(db.Integer,primary_key=True)
    #the class Task has id as primary key
    title = db.Column(db.String(120))
    #title with string at max 120
    status = db.Column(db.String(30))
    #status with string at max 120

#Multiple routes to handle different request from customers. 
#use decorator function to tell Flask what URL should trigger our function.
@app.route('/')
#define function index
def index():
    #query all data with different status
    todo_list = Task.query.filter_by(status="Todo").all()
    doing_list = Task.query.filter_by(status="Doing").all()
    done_list = Task.query.filter_by(status="Done").all()
    #display all data by using render_template, it takes in the variables we want to display and the main html page
    return render_template('base.html',todo_list=todo_list,doing_list= doing_list,done_list = done_list)

#define function about
@app.route('/about')
#This function is super simple and returns the following statement.
def about():
    return "Hello, this is CS162 Assignment."


#define the route /add that can be accessed with the method POST only.
@app.route("/add",methods=["POST"])
def add():
    #asking the form for what is inside the input named title in the base.html
    title = request.form.get("title")
    #variable new_task is equal to new instance of class Task with specified values as parameter.
    new_task = Task(title=title,status="Todo")
    #add the new variable new_task to the db.
    db.session.add(new_task)
    #commit the new change to the db.
    db.session.commit()
    #return the user to index(main page)
    return redirect(url_for("index"))

#define the route /update that can be accessed with the method POST only.
@app.route("/update/<int:todo_id>/<todo_status>",methods=["GET"])
def update(todo_id, todo_status):
    #asking the form for what is inside the input named title in the base.html
    title = request.form.get("title")
    #variable current_task is equal to new instance of class Task with specified values as parameter.
    current_task = Task.query.get(todo_id)
    current_task.status= todo_status
    #commit the new change to the db.
    db.session.commit()
    return redirect(url_for("index"))

#define the route /delete with specic id that can be accessed with the method POST,GET only.
@app.route("/delete/<int:todo_id>",methods=["POST","GET"])
def delete(todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    #delete variable todo in db
    db.session.delete(todo)
    #commit the new change to the db.
    db.session.commit()
    #redirect user to main page
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)