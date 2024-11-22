from typing import List

from flask import request
from flask_restful import Resource

from models.models import User
from repository.repository import UsersRepository


class UserRouter(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            user: User = UsersRepository.get_user_by_id(user_id)
            if user is None:
                return {'message': f'User with ID {user_id} does not exist'}, 404

            return user.__dict__(), 200

        return {'message': 'Bad request'}, 400

    def put(self, user_id=None):
        if user_id is None:
            return {'message': 'Bad request'}, 400

        user: User = UsersRepository.get_user_by_id(user_id)
        if user is None:
            return {'message': f'User with ID {user_id} does not exist'}, 404

        login = request.json['login']
        email = request.json['email']
        age = request.json['age']

        res: bool = UsersRepository.update_user(user_id, login, email, age)
        if res:
            return {'message': f'User with ID {user_id} updated successfully'}, 200
        else:
            return {'message': f'User with ID {user_id} does not exist'}, 404

    def delete(self, user_id=None):
        if user_id is None:
            return {'message': 'Bad request'}, 400

        res: bool = UsersRepository.delete_user(user_id)
        if res:
            return {'message': f'User with ID {user_id} deleted successfully'}, 200
        else:
            return {'message': f'User with ID {user_id} does not exist'}, 404


class UsersRouter(Resource):
    def get(self):
        users: List[User] = UsersRepository.get_users()
        response = []
        for user in users:
            response.append(user.__dict__())

        return {"users": response}, 200

    def post(self):
        login = request.json['login']
        email = request.json['email']
        age = request.json['age']

        user: User = User()
        user.login = login
        user.email = email
        user.age = age

        UsersRepository.create_user(user)
        return {'message': 'User created'}, 201
