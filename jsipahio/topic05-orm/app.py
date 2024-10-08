from flask import Flask, render_template, request, redirect, url_for
from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField


db = SqliteDatabase('pets.db')


class Kind(Model):
    kind_name = CharField()
    food = CharField()
    noise = CharField()
    class Meta:
        database = db


class Pet(Model):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref='pets')
    class Meta:
        database = db


db.connect()
db.create_tables([Pet, Kind])
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_pets():
    pets = Pet.select().join(Kind)
    return render_template("list.html", prof={'name':"john", 'class':'ADSD'}, pets=pets)


@app.route("/list/kinds")
def list_kinds():
    kinds = Kind.select()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/delete/<id>")
def get_delete(id):
    Pet.delete_by_id(id)
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
        kind = Kind.get_or_none(Kind.id == data["kind"])
        if kind is None:
            return "kind not found"
        Pet.create(name=data["name"], age=data["age"], owner=data["owner"], kind_id=kind)
        return redirect(url_for('list_pets',))
    if request.method == 'GET':
        rows = Kind.select()
        return render_template("create.html", rows=rows)
    

@app.route("/update/<id>", methods=['GET'])
def get_update(id):
    pet = Pet.get_or_none(Pet.id == id)
    if pet is None:
        return "pet not found"
    kinds = Kind.select()
    return render_template("update.html", pet=pet, kinds=kinds)


@app.route("/update", methods=['POST'])
def post_update():
    try:
        data = dict(request.form)
    except:
        return "Error updating pet. try again later"
    Pet.update({Pet.name:data["name"], 
                Pet.age:data["age"], 
                Pet.owner:data["owner"], 
                Pet.kind:Kind.get_by_id(data["kind"])}).where(Pet.id == data["id"]).execute()
    return redirect(url_for('list_pets'))


@app.route("/update/kind/<id>", methods=['GET'])
def get_kind_update(id):
    kind = Kind.get_or_none(Kind.id == id)
    if kind is None:
        return "kind not found"
    return render_template("kind_update.html", kind=kind)


@app.route("/update/kind", methods=["POST"])
def post_kind_update():
    try:
        data = dict(request.form)
    except:
        return "could not update kind"
    Kind.update({
        Kind.kind_name: data["name"],
        Kind.food: data["food"],
        Kind.noise: data["noise"]
    }).where(Kind.id == data["id"]).execute()
    return redirect(url_for("list_kinds"))


@app.route("/create/kind", methods=['GET', 'POST'])
def create_kind():
    if request.method == 'GET':
        return render_template("kind_create.html")
    elif request.method == 'POST':
        try:
            data = dict(request.form)
        except:
            return "request data missing"
        Kind.create(kind_name=data["name"], food=data["food"], noise=data["noise"])
        db.commit()
        return redirect(url_for("list_kinds"))
    else:
        return("invalid route")
    

@app.route("/delete/kind/<id>")
def delete_kind(id):
    Kind.delete_by_id(id)
    return(redirect(url_for("list_kinds")))