import db
from paths import db_path

class UserManager:
    def __init__(self):
        db.init_db()

    def create_user(self, name, email):
        query = 'INSERT INTO user (name, email) VALUES (?, ?)'
        db.execute_query(query, (name, email))

    def retrieve_all_users(self):
        query = 'SELECT id, name, email FROM user'
        results = db.execute_query(query)
        users = []
        for result in results:
            users.append({'id': result[0], 'name': result[1], 'email': result[2]})
        return users

    def retrieve_user(self, id):
        query = 'SELECT name, email FROM user WHERE id = ?'
        result = db.execute_query(query, (id,))
        if result:
            return {'id': id, 'name': result[0][0], 'email': result[0][1]}
        return None

    def update_user(self, id, name, email):
        query = 'UPDATE user SET name = ?, email = ? WHERE id = ?'
        db.execute_query(query, (name, email, id))

    def delete_user(self, id):
        query = 'DELETE FROM user WHERE id = ?'
        db.execute_query(query, (id,))