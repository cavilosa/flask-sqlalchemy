from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # the app gets named after the name of the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cavilosa1@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __rep__(self):
        return f"<Todo {self.id} {self.descriptions}>"

db.create_all()


@app.route("/")
def index():
    # empty = Todo.query.filter(Todo.description=="")
    # empty.delete()
    # db.session.commit()
    return render_template("index.html", data=Todo.query.all())


@app.route("/todos/create", methods=["POST"])
def create_todo():
    description = request.get_json()["description"]
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        "description": todo.description
    })

if __name__ == '__main__':
    app.run()
