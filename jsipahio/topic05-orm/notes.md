# Object Relation Mapper (ORM)

### What is it?
- tool to interact with DB using objects instead of queries
- map tables to classes
- map rows to instances of class
- Benefits
    - simplifies database interactions
    - cleaner, more maintainable code
    - abstracts away database-specific sql, making code more portable

## Common in Python
- SQLAlchemy
    - popular and powerful
    - advanced features
- Django ORM
    - simplicity and rapid dev
    - works off django
- PeeWee
    - lightweight
    - simple and easy to use
    - ideal for smaller projects

## PeeWee
- small
- light and simple
- support for sqlite, postgres, mysql
- When to Use?
    - easy to understand and setup
    - don't need complex features
```python
# create connection
from peewee import SqliteDatabase
db = SqliteDatabase('connection')


# create models
from peewee import Model, CharField, IntegerField, ForeignKeyField

# implicitely creates ID fields
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


# create tables
db.connect()
db.create_tables([Pet, Kind])


#insert new Kind
kind = Kind.create(kind_name="Dog", food="Kibble", noise="Bark")

#insert a new pet and link it to kind
pet = Pet.create(name="Buddy", age=3, owner="John Doe", kind=kind)

# retrieve
pets = Pet.select()

# join
pets_with_kind = Pet.select().join(Kind)

# print
for pet in pets_with_kind:
    print(f"{pet.name} is a {pet.kind.kind_name}")

# update
Pet.update({Pet.age: 4}).where(Pet.name == "Buddy").execute()

# delete
Pet.delete().where(Pet.name == "Buddy").execute()
# don't delete without a where clause...

# can use where() on select

```
## Recap
- simple
- efficient
- flexible
- supports foreign keys
- good for small to medium projects
- good starting point
- values simplicity over advanced ORM features

## SQL alchemy
```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declaratives import declaratives_base

Base = declaratives_base()

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
```