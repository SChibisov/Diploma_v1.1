from typing import List

from flask import request
from flask_restful import Resource

from models.models import Cart, User, Product
from repository.repository import CartRepository, UsersRepository, ProductsRepository


def _cart_from(user_id, product_id, product_count):
    cart = Cart()
    cart.user_id = user_id
    cart.product_id = product_id
    cart.product_cnt = product_count
    return cart


class CartRouter(Resource):
    def get(self, user_id=None):
        if user_id is None:
            return {'message': 'Bad request'}, 400

        carts: List[Cart] = CartRepository.get_cart_by_user_id(user_id)
        response = []
        for cart in carts:
            response.append(cart.__dict__())

        return {"carts": response}, 200

    def put(self, user_id=None):
        if user_id is None:
            return {'message': 'Bad request'}, 400

        user: User = UsersRepository.get_user_by_id(user_id)
        if user is None:
            return {'message': f'User with ID {user_id} does not exist'}, 404

        product_id = request.json['product_id']
        product_cnt = request.json['product_cnt']

        carts: List[Cart] = CartRepository.get_cart_by_user_id(user_id)

        current_cart: Cart = None
        is_new_cart: bool = False
        if len(carts) == 0:
            current_cart = _cart_from(user.id, product_id, product_cnt)
            is_new_cart = True
        else:
            for c in carts:
                if c.product_id == product_id and user.id == c.user_id:
                    current_cart = c
                    break

        if current_cart is None:
            current_cart = _cart_from(user.id, product_id, product_cnt)
            is_new_cart = True

        is_added = False
        products: List[Product] = ProductsRepository.get_products()

        for product in products:
            if product.is_available and product.id == product_id:
                current_count = product.product_cnt - product_cnt

                if current_count < 0:
                    break
                else:
                    ProductsRepository.update_product_count(product.id, current_count)
                    if product.product_cnt == 0:
                        ProductsRepository.update_product_availability(product.id, False)

                    if is_new_cart:
                        current_cart.product_count = product_cnt
                    else:
                        current_cart.product_count += product_cnt

                    is_added = True
                    break

        if is_added:
            if is_new_cart:
                CartRepository.create_cart(current_cart)
            else:
                CartRepository.update_cart(current_cart)

            return {"message": f"Cart for user with ID {user_id} updated successfully"}, 201

        return {"message": f"Cart for user with ID {user_id} does not exist"}, 404

    def delete(self, cart_id):
        if cart_id is None:
            return {'message': 'Bad request'}, 400

        res: bool = CartRepository.delete_cart(cart_id)
        if res:
            return {'message': f'Cart with ID {cart_id} deleted successfully'}, 200
        else:
            return {'message': f'Cart with ID {cart_id} does not exist'}, 404
