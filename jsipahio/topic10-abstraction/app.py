from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import database

app = Flask(__name__)


cnn = sqlite3.connect("pets.db", check_same_thread=False)
cnn.execute("PRAGMA foreign_keys = 1")

@app.route("/")
@app.route("/list")
def list_pets():
    # crs = cnn.cursor()
    # crs = cnn.cursor()
    # crs.execute('''
    #     select p.id, p.name, p.owner, p.age, 
    #         k.id, k.kind_name, k.food, k.noise 
    #     from pets p join kind k on p.kind_id = k.id
    # ''')
    # rows = crs.fetchall()
    rows = database.retrieve_list()
    print(rows)
    # print(rows)
    return render_template("list.html", prof={'name':"john", 'class':'ADSD'}, rows=rows)


@app.route("/list/kinds")
def list_kinds():
    rows = database.retrieve_kinds_list()
    return render_template("kind_list.html", rows=rows)


@app.route("/delete/<id>")
def get_delete(id):
    database.delete_pet(id)
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
        database.create_pet(request=request)
        return redirect(url_for('list_pets',))
    if request.method == 'GET':
        rows = database.get_kindID_Name()
        # print(rows)
        return render_template("create.html", rows=rows)
    

@app.route("/update/<id>", methods=['GET'])
def get_update(id):
    data = database.get_single_pet(id)
    # crs = cnn.cursor()
    # crs.execute("select id, kind_name from kind")
    # rows = crs.fetchall()
    # rows = [list(row) for row in rows]
    rows = database.get_kindID_Name()
    # print(rows)
    return render_template("update.html", data=data, rows=rows)


@app.route("/update", methods=['POST'])
def post_update():
    # print('hello')
    # crs = cnn.cursor()
    try:
        data = dict(request.form)
    except:
        return "Error updating pet. try again later"
    database.update_pet(data)
    return redirect(url_for('list_pets'))


@app.route("/update/kind/<id>", methods=['GET'])
def get_kind_update(id):
    data = database.get_single_kind(id)
    return render_template("kind_update.html", data=data)


@app.route("/update/kind", methods=["POST"])
def post_kind_update():
    try:
        data = dict(request.form)
        # print(data)
    except:
        return "error: did not receive data to do update"
    database.update_kind(data)
    return redirect(url_for("list_kinds"))


@app.route("/create/kind", methods=['GET', 'POST'])
def create_kind():
    if request.method == 'GET':
        return render_template("kind_create.html")
    elif request.method == 'POST':
        try:
            data = dict(request.form)
            # print(type(data))
        except:
            return "request data missing"
        database.create_kind(data)
        return redirect(url_for("list_kinds"))
    else:
        return("invalid route")
    

@app.route("/delete/kind/<id>")
def delete_kind(id):
    database.delete_kind(id)
    return(redirect(url_for("list_kinds")))