# ADSD: Joins and ACID

## Basic SQL
```sql
create table tblName
(
    col1 type, 
    col2 type, ...
);
```
```sql
insert into tblName(col1, col2,...)
values (val1, val2, ...)
```

## Selects & Joins
- single table
    - return subset of columns (projection)
    - return subset of rows (selection)
    - orders rows
    - groups rows
- multiple tabls
    - creates larger view onto both tables
    - "where" defines connection
### Join
- for multiple tables
- join on related columns  
**inner**
- only the related rows  
**outer**  
- everything (not all DBs implements)  
**left**
- all rows from left table whether there is match in left or not  
**right**
- opposite of left join  
**cross join**
- every possible combination  
## ACID
- atomic
- consistent
- isolated
- durable
### Atomic
- transactions completely handled or not handled
- no partial transactions
### Consistent
- all data meets constraints
    - example: all pets have a kind, must have kind on creation
- no violation states
    - no rest state where database will be at rest with inconsistency
- transaction locks
### Isolated
- concurrent transactions cannot see each other's state
- there must be a sequential equivalent
    - transactional analysis lets transactions be completed concurrently'
    - as if they were done one after another
### Durable
- any committed transaction must be permananent
- no excuses
- not even power outages or crashes
    - one operation to switch current state to permanent state and destroy old state

## Database API
- sqlite fiddle - play with sqlite db
## Homework
- show codespace running flask
- foreign keys