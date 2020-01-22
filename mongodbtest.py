from pymongo import MongoClient

conn = MongoClient('47.105.38.117', 27017)
db = conn.mydb
my_set = db.test_set
my_set.insert({"name":"zhangsan","age":18})