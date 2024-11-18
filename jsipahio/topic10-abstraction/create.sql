-- create tables

create table if not exists kind (
    id integer primary key autoincrement,
    kind_name text not null,
    food text not null,
    noise not null
);

create table if not exists pets (
    id integer primary key autoincrement,
    name text not null,
    age integer not null check (age >= 0),
    kind_id integer not null,
    owner text not null,
    foreign key(kind_id) references kind(id)
);

-- insert into kind (kind_name, food, noise)
-- values ('dog', 'dog food', 'bark'),
--     ('cat', 'cat food', 'meow'),
--     ('fish', 'fish flakes', 'blub');

insert into pets (name, age, kind_id, owner)
values ('dog1,', 4, 1, 'owner1'),
    ('cat1', 3, 2, 'owner2'),
    ('fish1', 1, 3, 'owner1');