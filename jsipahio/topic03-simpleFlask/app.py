from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


cnn = sqlite3.connect("pets.db", check_same_thread=False)


@app.route("/")
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
    return redirect(url_for('list_pets',))


@app.route("/hello")
def hello_world():
    return("<p>Hello there, World!</p>")


@app.route("/goodbye")
def goodbye():
    return ("<p>Goodbye, then! Have a nice day.")


@app.route("/create", methods=['GET', 'POST'])
def get_create():
    if request.method == 'POST':
        data = dict(request.form)
        crs = cnn.cursor()
        crs.execute("""
        insert into pets(name, type, age, owner)
        values (?,?,?,?)""",(data.get("name",""), data.get("type",""), int(data.get("age",0)), data.get("owner", ""),))
        cnn.commit()
        return redirect(url_for('list_pets',))
    if request.method == 'GET':
        return render_template("create.html")
    

@app.route("/update/<id>", methods=['GET'])
def get_update(id):
    crs = cnn.cursor()
    crs.execute("select * from pets where id = ?", (id,))
    data = crs.fetchone()
    return render_template("update.html", data=data)


@app.route("/update", methods=['POST'])
def post_update():
    print('hello')
    crs = cnn.cursor()
    try:
        data = request.form
    except:
        return "Error updating pet. try again later"
    crs.execute("""
    update pets
    set name = ?, type = ?, age = ?, owner = ?
    where id = ?""", (data["name"], data["type"], int(data["age"]), data["owner"], int(data["id"])))
    cnn.commit()
    return redirect(url_for('hello_world'))