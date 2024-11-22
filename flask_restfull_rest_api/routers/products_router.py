from typing import List

from flask import request
from flask_restful import Resource

from models.models import Product
from repository.repository import ProductsRepository


class ProductRouter(Resource):
    def get(self, product_id=None):
        if product_id is not None:
            product: Product = ProductsRepository.get_product(product_id)
            if product is None:
                return {'message': f'Product with ID {product_id} does not exist'}, 404

            return product.__dict__(), 200

        return {'message': f'Product with ID {product_id} does not exist'}, 404

    def put(self, product_id=None):
        if product_id is None:
            return {'message': 'Bad request'}, 400

        product: Product = ProductsRepository.get_product(product_id)
        if product is None:
            return {'message': 'Product does not exist'}, 404

        product_name = request.json['product_name']
        product_cnt = request.json['product_cnt']
        is_available = request.json['is_available']

        res: bool = ProductsRepository.update_product(product_id, product_name, product_cnt, is_available)
        if res:
            return {'message': f'Product with ID {product_id} updated successfully'}, 200
        else:
            return {'message': f'Product with ID {product_id} does not exist'}, 404

    def delete(self, product_id=None):
        if product_id is None:
            return {'message': 'Bad request'}, 400

        res: bool = ProductsRepository.delete_product(product_id)
        if res:
            return {'message': f'Product with ID {product_id} deleted successfully'}, 200
        else:
            return {'message': f'Product with ID {product_id} does not exist'}, 404


class ProductsRouter(Resource):
    def get(self):
        products: List[Product] = ProductsRepository.get_products();
        response = []
        for product in products:
            response.append(product.__dict__())

        return {"products": response}, 200

    def post(self):
        product_name = request.json['product_name']
        product_cnt = request.json['product_cnt']

        product: Product = Product()
        product.product_name = product_name
        product.product_cnt = product_cnt

        ProductsRepository.create_product(product)
        return {'message': 'Product created'}, 201
