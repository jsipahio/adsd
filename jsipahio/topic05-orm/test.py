from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField
import sqlite3

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

print(list(Kind.select(Kind.kind_name == 'dog')))