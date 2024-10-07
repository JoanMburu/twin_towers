from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.member_service import MemberService
from app.utils.authentication import authenticate_admin
from app.models.member import Member
from app import db


class MemberListResource(Resource):
    def get(self):
        """Get all members."""
        members = MemberService.get_all_members()
        return [member.to_dict() for member in members], 200

    @jwt_required()
    def post(self):
        """Create a new member."""
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        data = request.get_json()
        return MemberService.create_member(data)


class MemberResource(Resource):
    def get(self, id):
        """Get a single member by ID."""
        return MemberService.get_member_by_id(id)

    @jwt_required()
    def put(self, id):
        """Update a member by ID (admin-only)."""
        current_user = get_jwt_identity()
        
        if current_user['role'] != 'admin':
            return jsonify({"error": "Admin access required"}), 403

        member = Member.query.get(id)
        if not member:
            return {"error": "Member not found"}, 404

        data = request.get_json()
        if not data:
            return {"error": "Invalid request, no data provided"}, 400

        if 'phone' in data and Member.query.filter(Member.phone == data['phone'], Member.id != member.id).first():
            return {"error": "Phone number already exists"}, 400

        if 'email' in data and Member.query.filter(Member.email == data['email'], Member.id != member.id).first():
            return {"error": "Email address already exists"}, 400

        member.name = data.get('name', member.name)
        member.phone = data.get('phone', member.phone)
        member.email = data.get('email', member.email)
        member.role = data.get('role', member.role) 

        try:
            db.session.commit()
            return member.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": "An error occurred while updating the member", "details": str(e)}, 500

    @jwt_required()
    def delete(self, id):
        """Delete a member by ID."""
        return MemberService.delete_member(id)
