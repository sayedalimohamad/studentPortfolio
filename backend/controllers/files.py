from flask import Blueprint, request, jsonify
from extensions import db
from models import File, User
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_routes(bp: Blueprint):
    # Upload a new file
    @bp.route("/", methods=["POST"])
    @jwt_required()
    def upload_file():
        current_user = get_jwt_identity()
        data = request.get_json()
        # Auto-generate file_path based on file type
        file_type_folder = f"/path/to/{data['file_type']}s/"
        file_path = f"{file_type_folder}{data['file_name']}"

        file = File(
            user_id=current_user,
            file_name=data["file_name"],
            file_path=file_path,  # Use the auto-generated path
            file_type=data["file_type"],
            file_type_id=data["file_type_id"],
            visibility=data.get("visibility", "public"),
        )
        
        db.session.add(file)
        db.session.commit()
        return jsonify(file.to_dict()), 201

    # Get all files (filtered by privacy and user role)
    @bp.route("/all", methods=["GET"])
    @jwt_required()
    def get_all_files():
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        files = File.query.all()
        filtered_files = []

        for file in files:
            if file.visibility == "public":
                filtered_files.append(file.to_dict())
            elif file.visibility == "supervisors" and user.role in [
                "supervisor",
                "admin",
            ]:
                filtered_files.append(file.to_dict())
            elif file.visibility == "private" and file.user_id == current_user:
                filtered_files.append(file.to_dict())

        return jsonify(filtered_files)

    # Get files uploaded by the current user
    @bp.route("/my-files", methods=["GET"])
    @jwt_required()
    def get_my_files():
        current_user = get_jwt_identity()
        files = File.query.filter_by(user_id=current_user).all()
        return jsonify([file.to_dict() for file in files])

    # Get a specific file by ID
    @bp.route("/<int:file_id>", methods=["GET"])
    @jwt_required()
    def get_file(file_id):
        file = File.query.get_or_404(file_id)
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        # Check file visibility
        if file.visibility == "private" and file.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403
        if file.visibility == "supervisors" and user.role not in [
            "supervisor",
            "admin",
        ]:
            return jsonify({"error": "Unauthorized"}), 403

        return jsonify(file.to_dict())

    # Update a file
    @bp.route("/<int:file_id>", methods=["PUT"])
    @jwt_required()
    def update_file(file_id):
        file = File.query.get_or_404(file_id)
        current_user = get_jwt_identity()
        if file.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        file.file_name = data.get("file_name", file.file_name)
        file.file_path = data.get("file_path", file.file_path)
        file.file_type = data.get("file_type", file.file_type)
        file.file_type_id = data.get("file_type_id", file.file_type_id)
        file.visibility = data.get("visibility", file.visibility)
        db.session.commit()
        return jsonify(file.to_dict())

    # Delete a file
    @bp.route("/<int:file_id>", methods=["DELETE"])
    @jwt_required()
    def delete_file(file_id):
        file = File.query.get_or_404(file_id)
        current_user = get_jwt_identity()
        if file.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(file)
        db.session.commit()
        return "", 204
