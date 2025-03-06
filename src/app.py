from flask import Flask, request,url_for,render_template,jsonify
from configs.config import FlaskAppConfig
from src.core import validation_logic as vl

app:Flask = Flask(__name__)
app.config.from_object(FlaskAppConfig)

from flask_sqlalchemy import SQLAlchemy

#Init Database--------------------------------------------------
db=SQLAlchemy()
db.init_app(app=app)

#Declare Table--------------------------------------------------
class TodoTable(db.Model):
    # init table name and type of columns
    __tablename__="todos"
    id= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(255),nullable=False)
    isCompleted = db.Column(db.Boolean, default=False)

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

#----------APIS these will be called by vanilla JS---------------
@app.route("/add_todo",methods=["POST"])
def add_todo():
    content=request
    try:
        title=vl.validate_title(content)
        new_task=TodoTable(title=title)
        db.session.add(new_task)
        db.session.commit()


        return (jsonify({"status":200,"message":f"New Task added- {new_task.to_dict()}"}))
    except ValueError as e:
        pass
        # do nothing if error
        return jsonify({"message":"some errr"})

@app.route("/delete_todo",methods=["POST"])
def delete_todo():
    content=request
    try:
        todo_id=content["id"]
        todo=TodoTable.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()

        return (jsonify({"status":200,"message":f"Task deleted"}))
    except ValueError as e:
        pass
        # do nothing if error
        return jsonify({"message":"some errr"})

@app.route("/toggle_isCompleted",methods=["POST"])
def toggle_isCompleted():
    content=request
    try:
        todo_id=content["id"]
        todo=TodoTable.query.get(todo_id)
        todo.isCompleted= not todo.isCompleted

        db.session.delete(todo)
        db.session.commit()
        
        return (jsonify({"status":200,"message":f"Task deleted"}))
    except ValueError as e:
        pass
        # do nothing if error
        return jsonify({"message":"some errr"})

#---------------------------------------------------------------------------
@app.route('/')
def index():
    tasks = TodoTable.query.all()
    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
