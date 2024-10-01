# SQL Alchemy

## Object Relation mapper
- create map between data and objects
    - create table -> class init
    - create record -> object init
    - update,delete -> object methods
    - searches -> class methods using object descriptions
    - key enforcements -> relationship management

## SQL Alchemy
- descendent of SQLObject
- allows declaration of python classes
- create tables, indices
- validate data
- manages foreign keys, composite keys
- (relatively) easy to use
- moves in direction of NoSQL - think about application objects, not rows of data

```python
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"string representation of data"


```

```bash
$ python
>>> Base.metadata.create_all(engine)
PRAGMA table_info("users") ...
```

- Function based queries

```python
session.query(User).filter_by(name="ed").first()
session.add_all([
    User(name="wendy", fullname="wendy williams", password="badpass"),
    User(name="mary", fullname="mary contrary", password="xxg527"),
    User(name="fred", ...)
])
```
- separation of mapping and class
    - manual mapping
    - allows any class to map to any table
    - "declarative" mapping is default
    - free to invent own
        - handy if classes or tables already exist
- self referential mapping
    - can load subrecords, even if they are part of chain
    - many-to-many can be loaded
    - depth management

### Resources
- https://www.sqlachemy.org



