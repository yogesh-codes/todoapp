from flask import Flask, request,url_for,render_template,jsonify,redirect,flash
from src.core.config import FlaskAppConfig,context_variables
from src.core import validation_logic as vl


app:Flask = Flask(__name__)
app.config.from_object(FlaskAppConfig)

import os
app.secret_key = os.urandom(24)

from flask_sqlalchemy import SQLAlchemy

#INITIALIZATIONS=================================================

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
    
    try:
        title=request.form.get("title")
        title=vl.validate_and_clean_title(title)
        new_todo=TodoTable(title=title)
        db.session.add(new_todo)
        db.session.commit()


        #return (jsonify({"status":200,"message":f"New Task added- {new_task}"}))
        flash(f"'{title}' was added","success")
        
    except ValueError as e:
        
        #return jsonify({"message":str(e)})
        flash(f"Error on adding todo {title}-{str(e)}","fail")
        
    finally:
        return redirect(url_for("index"))

@app.route("/delete_todo",methods=["POST"])
def delete_todo():
    try:
        content=request.get_data()
        todo_id=content["id"]
        vl.validate_and_obtain_todoid(todo_id)
        todo=TodoTable.query.get(todo_id)
        title=todo.title
        db.session.delete(todo)
        db.session.commit()

    
        flash(category="success",message=f"deleted todo- {title}")
    except ValueError as e:
        
        flash(category="fail",message=f"Failed to delete- {str(e)}")

    finally:
        redirect(url_for("index"))
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
    return context_variables

#per app
@app.route('/',methods=["GET"])
def index():
    todos = TodoTable.query.all()
    return render_template('index.html', todos=todos)

@app.route('/userprofile',methods=["GET"])
def userprofile():
    tasks = TodoTable.query.all()
    return render_template('userprofile.html', userprofile={"name":"Yogesh","age":100})

if __name__ == '__main__':
    new_task = TodoTable(title="Buy groceries", isCompleted=False)
    db.session.add(new_task)
    db.session.commit()
    app.run(debug=True)
