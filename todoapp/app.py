from flask import Flask, render_template

app = Flask(__name__) # the app gets named after the name of the file

@app.route("/")
def index():
    return render_template("index.html", data=[
        {"description": "Todo 1"},
        {"description": "Todo 2"},
        {"description": "Todo 3"},
        {"description": "Todo 4"}
        ])

if __name__ == '__main':
    app.run()
