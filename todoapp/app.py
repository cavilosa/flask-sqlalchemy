from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request

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
    return render_template("index.html", data=Todo.query.all())

@app.route("/create", methods=["POST"])
def create():
    list = Todo.query.all()
    todo = request.form.get("todo")
    if todo in list and todo != "":
        return render_template("index.html", data=Todo.query.all())
    else:
        item = Todo(description=todo)
        db.session.add(item)
        db.session.commit()

        return render_template("index.html", data=Todo.query.all())


if __name__ == '__main__':
    app.run()
