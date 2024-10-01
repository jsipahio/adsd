# Pony ORM
- write the database with lambda functions/generators

```python
select(c for c in Customer if sum(c.orders.total_price) > 1000)
```

