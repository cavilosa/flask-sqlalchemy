from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__) # the app gets named after the name of the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cavilosa1@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'),
                nullable=False)

    def __rep__(self):
        return f"<Todo {self.id} {self.descriptions}>"

#db.create_all() - migrations will do it for us?

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship('Todo', cascade="all, delete-orphan", backref='list', lazy=True)


@app.route("/lists/<list_id>")
def get_list_todos(list_id):
    # empty = Todo.query.filter(Todo.description=="")
    # empty.delete()
    # db.session.commit()
    return render_template("index.html",
    lists=TodoList.query.order_by("id").all(),
    active_list = TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by("id").all())


@app.route("/")
def index():
    return redirect(url_for('get_list_todos', list_id = 1))


@app.route("/todos/<todo_id>/delete", methods=["POST"])
def delete_item(todo_id):
    error = False
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({"success":True})
    # return jsonify({ 'success': True })
    #return redirect(url_for('index'))
    #return render_template("index.html")


@app.route("/lists/<delete_id>/delete", methods=["POST"])
def delete_list(delete_id):
    error = False
    try:
        list = TodoList.query.get(delete_id)
        for todo in list.todos:
            db.session.delete(todo)
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abourt(500)
    else:
        return jsonify({"success": True})


@app.route("/todos/<todo_id>/set-completed", methods=["POST"])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        print("todo: ", todo)
        todo.completed = completed # completed property comes from AXAJ request
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for("index"))


@app.route("/lists/<list_id>/set-completed", methods=["POST"])
def set_completed_list(list_id):
    try:
        completed = request.get_json()["completed"]
        list = TodoList.query.get(list_id)
        list.completed = completed
        todos=Todo.query.filter_by(list_id=list_id).order_by("id").all()
        for todo in todos:
            todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return '', 200


@app.route("/todos/create", methods=["POST"])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()["description"]
        list_id = request.get_json()["list_id"]
        todo = Todo(description=description,  list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body["description"] = todo.description
        # body["id"] = todo.id
        # body["complete"] = todo.complete
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route("/lists/<list_name>/create", methods=["POST"])
def create_list(list_name):
    error = False
    body ={}
    try:
        name = request.get_json()["name"]
        list = TodoList(name=list_name)
        db.session.add(list)
        db.session.commit()
        body["name"] = list.name
        # body["id"] = list.idea
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)



if __name__ == '__main__':
    app.run()
