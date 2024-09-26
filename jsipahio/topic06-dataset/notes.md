# Dataset module
- don't confuse with datasets
- databases for lazy people (that's me!)

- simplify database usage
- abstracts away SQL and is simple API
- features:
    - no need for schema
    - automatically creates tables and fields
    - provides pythonic access to tables as if they are lists dictionaries

## why?
- ease of use
- flexible
- minimal setup
- ideal for
    - simple projects
    - prototypes
    - minimal overhead to interact with databases

- suppored dbs
    - sqlite, postgresql, mysql, etc
- easy to switch between engines by changing connection string

## connections and use
```python
import dataset
# -------------------
# create connection
#--------------------

db = dataset.connect('sqlite:///pets.db')
# connect() establishes connection
# connection string determines the type of database, i.e. sqlite://, postgres://

# -------------------
# defining tables
#--------------------

# if table doesn't exist it creates it
table = db['pets']

kind_table = db['kind']
# tables don't exist until a column/data is added

# -------------------
# inserting data
#--------------------

#insert some data
kind_table.insert({
    'kind_name': 'dog',
    'food', 'kibble',
    'noise', 'bark'
})

table.insert({
    'name': 'buddy',
    'age': 3,
    'owner': 'john doe',
    'kind_id': 1 # foreign key to kind table
})

# no foreign key constraints, code must check for violations
# dataset good for reading, single tables
# not good for ACID

# ----------------
# select
#-----------------
pets = table.all()

older_pets = table.find(age={'>':2})

for pet in older_pets:
    print(f"{pet['name']} is {pet['age']} years old.")
# results are returned as dictionaries -> dict access

# ----------------
# update
#-----------------

table.update({
    'id': 1,
    'age': 4
}, ['id'])
# id of 1 exists, use it to find which record to update
# update age, set it to 4
# update not common use case of dataset

# ----------------
# delete
#-----------------
table.delete(id=1)
# delete from pets where id = 1

# ----------------
# relations
#-----------------
pets = table.all()

for pet in pets:
    kind = kind_table.find_one(id=pet['kind_id'])
    print(f"{pet['name']} is a {kind['kind_name']}.")
# manually join by retrieving matching record from related table

```

## with Flask
```python
# boilerplate stuff...

@app.route('/list')
def get_list():
    pets = db['pets'].all()
    return render_template("list.html", pets=pets)
# ...

```

## compared to full ORM
- setup : low vs defining models
- flexibility: high vs explicit schema definition
- use cases: simple, quick projects vs complex apps
- performance: lightweight vs more overhead from ORM features
- schema: implicit vs explicit

## when to use
### dataset
- prototyping
- small project
- don't want to write schema/sql

### ORM
- manage complex relationships
- working on large-scale apps where schema and performance control are critical

## transactions
- use with

```python
with dataset.connect() as tx:
    tx['user'].insert(dict(name='john doe', age=46, country='china'))
```

- use begin/commit/rollback

```python
db = dataset.connect()
db.begin()
try:
    db['user'].insert(dict(name='john doe', age=46, country='china'))
    db.commit()
except:
    db.rollback()
```
- can also nest transactions

## query
- can use `query` to direct query a database
- returns rows
- pretty much readonly

## conclusion
- good for small
- better for looking than modifying
- bad for big