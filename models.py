class User:
    def __init__(self, public_id, name, username, email, password):
        self.public_id = public_id
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
