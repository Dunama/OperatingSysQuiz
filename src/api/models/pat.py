from flask import request
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from src.db.models.quiz_db import Pat
from src.db.core import db

# blue print for pat CRUD
pat_bp = Blueprint('pat', __name__)
api = Api(pat_bp)

Patparser = reqparse.RequestParser()
Patparser.add_argument("name", type=str, required=True, help='Name is required')

@pat_bp.route('/pat', methods=['POST'])
def post():
    '''create a participant'''
    args = Patparser.parse_args()
    new_pat = Pat(name=args['name'])
    db.session.add(new_pat)
    db.session.commit()
    return {'message': 'Participant Registered Successfully'},200

@pat_bp.route('/pat', methods=['GET'])   
def get():
    '''get all participants'''
    pats = Pat.query.all()
    if not pats:
        return {'message': 'No participants found'}
    pat_list = []
    for  pat in pats:
        pat_list.append({
            'id': pat.id,
            'name': pat.name
        })
    return {'participants': pat_list}

@pat_bp.route('/pat/<int:pat_id>', methods=['GET'])
def get_by_id(pat_id):
    '''get a participant by id'''
    pat = Pat.query.get(pat_id)
    if not pat:
        return {'message': 'Participant not found'}, 404
    
    pat_id = {
        'id': pat.id,
        'name': pat.name
    }
    return {'participant': pat_id},201

@pat_bp.route('/pat/<int:pat_id>', methods=['PUT'])
def put(pat_id):
    '''update a participant'''
    args = Patparser.parse_args()
    pat = Pat.query.get(pat_id)
    if not pat:
        return {'message': 'Participant not found'}, 404
    if args['name'] is not None:
        pat.name = args['name']

        update_pat = {
            'id': pat.id,
            'name': pat.name
        }
        db.session.commit()
        return {'message': 'Participant updated successfully', 'participant': update_pat},201
    
@pat_bp.route('/pat/<int:pat_id>', methods=['DELETE'])
def delete(pat_id):
    '''delete a participant'''
    pat = Pat.query.get(pat_id)
    if not pat:
        return {'message': 'Participant not found'}, 404
    delete_pat = {
        'id': pat.id,
        'name': pat.name
    }
    db.session.delete(pat)
    db.session.commit()
    return {'message': 'Participant deleted successfully', 'participant': delete_pat},201