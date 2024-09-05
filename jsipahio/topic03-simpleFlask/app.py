from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


cnn = sqlite3.connect("pets.db", check_same_thread=False)


@app.route("/list")
def list_pets():
    # crs = cnn.cursor()
    crs = cnn.cursor()
    crs.execute('select * from pets')
    rows = crs.fetchall()
    rows = [list(row) for row in rows]
    print(rows)
    return render_template("list.html", prof={'name':"john", 'class':'ADSD'}, rows=rows)

@app.route("/delete/<id>")
def get_delete(id):
    crs = cnn.cursor()
    crs.execute("delete from pets where id=?", (id,))
    cnn.commit()
    return f"<p>Trying to delete id = {id}</p>"

@app.route("/")
@app.route("/hello")
def hello_world():
    return("<p>Hello there, World!</p>")

@app.route("/goodbye")
def goodbye():
    return ("<p>Goodbye, then! Have a nice day.")