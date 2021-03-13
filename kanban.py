
from flask import Flask,url_for,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#create a class that 
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    status = db.Column(db.String(30))
    
@app.route('/')
def index():
    #shows all todo
    todo_list = Task.query.filter_by(status="Todo").all()
    doing_list = Task.query.filter_by(status="Doing").all()
    done_list = Task.query.filter_by(status="Done").all()
    #print(todo_list)
    return render_template('base.html',todo_list=todo_list,doing_list= doing_list,done_list = done_list)
#def add()

@app.route('/about')
def about():
    return "Hello, this is CS162 Assignment."
#function add    
@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title,status="Todo")
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>/<todo_status>",methods=["GET"])
def update(todo_id, todo_status):
    title = request.form.get("title")
    current_task = Task.query.get(todo_id)
    current_task.status= todo_status
    db.session.commit()
    return redirect(url_for("index"))

#
@app.route("/delete/<int:todo_id>",methods=["POST","GET"])
def delete(todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))




if __name__ == "__main__":
    db.create_all()
    # new_todo = Todo(title="Clean",do_ing= False,com_plete = False)
    # db.session.add(new_todo)
    # db.session.commit()
    app.run(debug=True)