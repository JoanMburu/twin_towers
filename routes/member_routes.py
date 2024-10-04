from flask import Blueprint, request, jsonify
from models.member import Member
from utils.authentication import authenticate_admin
from models import db 

member_bp = Blueprint('member_bp', __name__)

@member_bp.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([member.to_dict() for member in members]), 200

@member_bp.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member.to_dict()), 200

@member_bp.route('/members', methods=['POST'])
def create_member():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, no data provided"}), 400

    required_fields = ['name', 'phone', 'email', 'role']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"'{field}' is required"}), 400

    if Member.query.filter_by(phone=data["phone"]).first():
        return jsonify({"error": "Phone number already exists"}), 400
    if Member.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email address already exists"}), 400


    try:
        member = Member(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            role=data.get('role', 'member')  
        )


        db.session.add(member)
        db.session.commit()  

        return jsonify(member.to_dict()), 201

    except Exception as e:
   
        db.session.rollback()

        return jsonify({"error": "An error occurred while creating the member", "details": str(e)}), 500

    finally:
        db.session.close()


@member_bp.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    authenticate_admin()
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    if Member.query.filter(Member.phone == data["phone"], Member.id != member.id).first():
        return jsonify({"error": "Phone number already exists"}), 400
    if Member.query.filter(Member.email == data["email"], Member.id != member.id).first():
        return jsonify({"error": "Email address already exists"}), 400

    member.name = data.get("name", member.name)
    member.phone = data.get("phone", member.phone)
    member.email = data.get("email", member.email)

    db.session.commit()
    return jsonify(member.to_dict()), 200

@member_bp.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()

    return jsonify({"message": f"Member with id {id} has been deleted."}), 200




