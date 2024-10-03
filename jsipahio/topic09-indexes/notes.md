# Indexes
- indexes for database
- indices for math and science contexts

## Query Optimization
Tables vs Indexes  
- table is set of records
- index is a tree that can be searched
    - by single field
    - by multiple fields
- the tree result is an index (i.e. row number)
Indexes are important

### Optimizer strategies
SQL - create indexes at design  
Mongo - ad hoc indexes  
view images on sqlite page on search optimization  

```SQL
select price from FruitsForSale where fruit = 'peach'
```
- full table scan searches linearly until it finds peach, then gets the price
```SQL
select price from fruitsforsale where rowid=4
```
- row number fetch: row can be found in constant time if it is known
```SQL
create index idx1 on fruits(fruit)
```
- now searching by name does binary search to get rowid, then do rowid search
```SQL
select price from fruits where fruit = 'orange'
```
- tree traversal if there are multiple rows
```SQL
and state='CA'
```
- perform linear search on subset returned by index search
```SQL
create index idx2 on fruits(state)
```
- secondary index
- search idx2 then perform linear search on returned rows
```SQL
create index idx3 on fruits(fruit, state)
```
- build index on multiple columns
- only effective if searching on fruit **AND** state is common
- if only searching on one of the columns, performance suffers
- can be done
- more columns make it harder to maintain
- indexes only use the first value
```SQL
create index idx4 on fruits(fruit, state, price)
```
- a covering index
- contains all data needed to resolve a query
### OR search
- union results from two index searches
### AND search
- intersect results from two index search
## Sorting
```SQL
select * from fruits order by fruit
```
- nlog(n) sort
- sorting without an index
- ordering by rowid just prints table how it is
- sorting with index: index is maintained in order, just return the row ids in order
- covering index sort is trivial
- partial sorting by index
    - `sort by fruit, price`
    - may result in some data being out of order
    - send partially sorted sets to sorter
    - similar to a merge sort

## Sample databases
https://www.datablist.com/learn/csv/download-sample-csv-files