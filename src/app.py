from flask import Flask, request,url_for,render_template,jsonify
from src.core.config import FlaskAppConfig
from src.core import validation_logic as vl


app:Flask = Flask(__name__)
app.config.from_object(FlaskAppConfig)

from flask_sqlalchemy import SQLAlchemy

#INITIALIZATIONS=================================================
social_links={"LinkedIn":"https://www.linkedin.com/in/yogeshvperumal/",
              "GitHub":"https://github.com/yogesh-codes"}

#===Init Database
db=SQLAlchemy()
db.init_app(app=app)

#===Declare Table
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

#Create all table instance
with app.app_context():
    db.create_all()


#APIS these will be called by frontend (static JS)===================

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

#PAGE RENDERERS-----------------------------------------
## things that need to be shared to all apps
@app.context_processor
def context_processor():
    return {"social_links":social_links}

#per app
@app.route('/',methods=["GET"])
def index():
    tasks = TodoTable.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/userprofile',methods=["GET"])
def userprofile():
    tasks = TodoTable.query.all()
    return render_template('userprofile.html', userprofile={"name":"Yogesh","age":100})


if __name__ == '__main__':
    app.run(debug=True)
