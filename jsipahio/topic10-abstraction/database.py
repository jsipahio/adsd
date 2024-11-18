import sqlite3
from pprint import pprint

cnn = sqlite3.connect("pets.db", check_same_thread=False)
cnn.execute("PRAGMA foreign_keys = 1")


def retrieve_list():
    crs = cnn.cursor()
    crs.execute('''
        select p.id, p.name, p.owner, p.age, 
            k.id, k.kind_name, k.food, k.noise 
        from pets p join kind k on p.kind_id = k.id
    ''')
    rows = crs.fetchall()
    rows = [list(row) for row in rows]
    return rows


def retrieve_kinds_list():
    crs = cnn.cursor()
    crs.execute('select * from kind')
    rows = crs.fetchall()
    rows = [list(row) for row in rows]
    return rows


def delete_pet(id):
    crs = cnn.cursor()
    crs.execute("delete from pets where id=?", (id,))
    cnn.commit()
    return


def delete_kind(id):
    crs = cnn.cursor()
    crs.execute("delete from kind where id = ?", id)
    cnn.commit()


def create_pet(request):
        data = dict(request.form)
        # print(data)
        crs = cnn.cursor()
        crs.execute("""
        insert into pets(name, kind_id, age, owner)
        values (?,?,?,?)""",(data.get("name",""), int(data.get("kind",0)), int(data.get("age",0)), data.get("owner", ""),))
        cnn.commit()


def get_kindID_Name():
        crs = cnn.cursor()
        crs.execute("select id, kind_name from kind")
        rows = crs.fetchall()
        rows = [list(row) for row in rows]
        return rows


def get_single_pet(id):
    crs = cnn.cursor()
    crs.execute("select * from pets where id = ?", (id,))
    data = crs.fetchone()
    return data


def update_pet(data):
    crs = cnn.cursor()
    crs.execute("""
    update pets
    set name = ?, kind_id = ?, age = ?, owner = ?
    where id = ?"""
    , (data["name"], int(data["kind"]), int(data["age"]), data["owner"], int(data["id"])))
    cnn.commit()
    return


def get_single_kind(id):
    crs = cnn.cursor()
    crs.execute("select id, kind_name, food, noise from kind where id = ?", id)
    data = crs.fetchone()
    return data


def update_kind(data):
    crs = cnn.cursor()
    crs.execute("""
        update kind
        set kind_name = ?,
            food = ?,
            noise = ?
        where id = ? 
    """, (data["name"], data["food"], data["noise"], data["id"]))
    cnn.commit()
    return


def create_kind(data):
    crs = cnn.cursor()
    crs.execute("""
    insert into kind(kind_name, food, noise)
    values(?, ?, ?)
    """, (data["name"], data["food"], data["noise"]))
    cnn.commit();
    return


def test_retrieve_list():
    rows = retrieve_list()
    pprint(rows)
    exit()


if __name__ == "__main__":
    test_retrieve_list()