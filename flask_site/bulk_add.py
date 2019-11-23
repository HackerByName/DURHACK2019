from mongo import MongoDatabase
from __init__ import student_records, transaction_records
from random import randrange

record = student_records.find_one({"first_name": "Finlay", "last_name": "Boyle"})

for i in range(20):
    f = randrange(-1000, 1000)
    MongoDatabase.create_new_transaction(transaction_records, record["_id"], "personal", f)
