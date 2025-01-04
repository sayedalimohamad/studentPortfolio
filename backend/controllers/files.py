from flask import Blueprint, request, jsonify
from extensions import db
from models import File

def register_routes(bp: Blueprint):
    @bp.route('/files', methods=['POST'])
    def upload_file():
        data = request.get_json()
        file = File(
            user_id=data['user_id'],
            file_name=data['file_name'],
            file_path=data['file_path'],
            file_type=data['file_type'],
            file_type_id=data['file_type_id'],
            visibility=data['visibility']
        )
        db.session.add(file)
        db.session.commit()
        return jsonify(file.to_dict()), 201

    @bp.route('/files/<int:file_id>', methods=['GET'])
    def get_file(file_id):
        file = File.query.get_or_404(file_id)
        return jsonify(file.to_dict())

    @bp.route('/files/<int:file_id>', methods=['PUT'])
    def update_file(file_id):
        data = request.get_json()
        file = File.query.get_or_404(file_id)
        file.file_name = data.get('file_name', file.file_name)
        file.file_path = data.get('file_path', file.file_path)
        file.file_type = data.get('file_type', file.file_type)
        file.file_type_id = data.get('file_type_id', file.file_type_id)
        file.visibility = data.get('visibility', file.visibility)
        db.session.commit()
        return jsonify(file.to_dict())

    @bp.route('/files/<int:file_id>', methods=['DELETE'])
    def delete_file(file_id):
        file = File.query.get_or_404(file_id)
        db.session.delete(file)
        db.session.commit()
        return '', 204