from flask import request
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from src.db.models.quiz_db import User as user
from src.db.core import db

# blue print for user CRUD
user_bp = Blueprint('user', __name__)
api = Api(user_bp)

userparser = reqparse.RequestParser()
userparser.add_argument("name", type=str, required=True, help='Name is required')

@user_bp.route('/user', methods=['POST'])
def post():
    '''create a user'''
    args = userparser.parse_args()
    new_user = user(name=args['name'])
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'user Registered Successfully'},200

@user_bp.route('/user', methods=['GET'])   
def get():
    '''get all users'''
    users_record = user.query.all()
    if not users_record:
        return {'message': 'No users found'}
    user_list = []
    for  user in users_record:
        user_list.append({
            'id': user.id,
            'name': user.name
        })
    return {'users': user_list}

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_by_id(user_id):
    '''get a user by id'''
    user_record = user.query.get(user_id)
    if not user_record:
        return {'message': 'user not found'}, 404
    
    user_id = {
        'id': user.id,
        'name': user.name
    }
    return {'user': user_id},201

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def put(user_id):
    '''update a user'''
    args = userparser.parse_args()
    user_record = user.query.get(user_id)
    if not user_record:
        return {'message': 'user not found'}, 404
    if args['name'] is not None:
        user.name = args['name']

        update_user = {
            'id': user.id,
            'name': user.name
        }
        db.session.commit()
        return {'message': 'user updated successfully', 'user': update_user},201
    
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    '''delete a user'''
    user_record = user.query.get(user_id)
    if not user_record:
        return {'message': 'user not found'}, 404
    delete_user = {
        'id': user.id,
        'name': user.name
    }
    db.session.delete(user)
    db.session.commit()
    return {'message': 'user deleted successfully', 'user': delete_user},201