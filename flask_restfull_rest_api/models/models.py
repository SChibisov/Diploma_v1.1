class User:
    id: int
    login: str
    email: str
    age: int

    def __dict__(self):
        return {
            'id':       self.id,
            'login':    self.login,
            'email':    self.email,
            'age':      self.age
        }


class Product:
    id: int
    product_name: str
    product_cnt: int
    is_available: bool = True

    def __dict__(self):
        return {
            'id':           self.id,
            'product_name': self.product_name,
            'product_cnt':  self.product_cnt,
            'is_available': self.is_available
        }


class Cart:
    id: int
    user_id: int
    product_id: int
    product_name: str
    product_count: int

    def __dict__(self):
        return {
            'id':               self.id,
            'user_id':          self.user_id,
            'product_id':       self.product_id,
            'product_name':     self.product_name,
            'product_count':    self.product_count
        }
