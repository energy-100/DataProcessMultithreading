import redis

# 普通连接
conn = redis.Redis(host="47.105.38.117", port=6379)
conn.set("x1","hello",ex=5) # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)