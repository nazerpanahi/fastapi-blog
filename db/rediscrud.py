from redis import Redis


class RedisCRUD:
    def __init__(self, db: Redis):
        self.db = db

    def set(self, key, value):
        return self.db.set(key, value)

    def setex(self, key, time, value):
        return self.db.setex(key, time, value)

    def get(self, key):
        return self.db.get(key)

    def expire(self, key, time):
        return self.db.expire(key, time)

    def delete(self, *keys):
        return self.db.delete(*keys)

    def exists(self, *keys):
        return self.db.exists(*keys)
