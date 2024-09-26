import dataset 

def get_all(tbl):
    return [dict(d) for d in list(tbl.all())]

db = dataset.connect("sqlite:///:memory:")

table = db['sometable']
table.insert(dict(name='john doe', age=37))
table.insert(dict(name='jane doe', age=34, gender='female'))

john = table.find_one(name="john doe")
john = dict(john)

people = get_all(table)

print(people)