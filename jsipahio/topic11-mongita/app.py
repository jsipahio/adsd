from flask import Flask, render_template, request, redirect, url_for
import database as db

app = Flask(__name__)


@app.route("/")
@app.route("/pets")
def get_pets():
    pets = db.get_all_pets_join_kinds()
    return render_template("pets.html", pets=pets)


@app.route("/pets/create", methods=['GET', 'POST'])
def create_pet():
    if request.method == 'GET':
        kinds = db.get_all_kinds_simple()
        return render_template("create_pet.html", kinds=kinds)
    else:
        data = dict(request.form)
        db.create_pet(data)
        return redirect(url_for('get_pets'))
    

@app.route("/pets/update/<id>", methods=['GET', 'POST'])
def update_pet(id):
    if request.method == 'GET':
        pet = db.get_single_pet(id)
        kinds = db.get_all_kinds_simple()
        return render_template("update_pet.html", pet=pet, kinds=kinds)
    else:
        data = dict(request.form)
        db.update_pet(data)
        return redirect(url_for('get_pets'))
    

@app.route("/pets/delete/<id>")
def delete_pet(id):
    db.delete_pet(id)
    return redirect(url_for('get_pets'))


@app.route("/kinds")
def get_kinds():
    kinds = db.get_all_kinds()
    return render_template("kinds.html", kinds=kinds)


@app.route("/kinds/create", methods=['GET', 'POST'])
def create_kind():
    if request.method == "GET":
        return render_template("create_kind.html")
    else:
        data = dict(request.form)
        db.create_kind(data)
        return redirect(url_for("get_kinds"))
    

@app.route("/kinds/update/<id>", methods=['GET', 'POST'])
def update_kind(id):
    if request.method == 'GET':
        kind = db.get_single_kind(id)
        return render_template("update_kind.html", kind=kind)
    else:
        data = dict(request.form)
        db.update_kind(data)
        return redirect(url_for('get_kinds'))
    

@app.route("/kinds/delete/<id>")
def delete_kind(id):
    result = db.delete_kind(id)
    if result:
        return redirect(url_for("get_kinds"))
    else:
        return "<p>could not delete kind. there are still pets that use this kind.</p>"
