from app.repositories.member_repository import MemberRepository
from app.models.member import Member

class MemberService:
    @staticmethod
    def get_all_members():
        return MemberRepository.get_all_members()

    @staticmethod
    def get_member_by_id(id):
        member = MemberRepository.get_member_by_id(id)
        if not member:
            return {"error": "Member not found"}, 404
        return member.to_dict(), 200

    @staticmethod
    def create_member(data):
        required_fields = ['name', 'phone', 'email', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"'{field}' is required"}, 400

        if MemberRepository.find_by_email_or_phone(data['email'], data['phone']):
            return {"error": "Email or Phone already exists"}, 400

        try:
            member = Member(
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                role=data.get('role', 'member')
            )
            MemberRepository.create_member(member)
            return member.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_member(id, data):
        member = MemberRepository.get_member_by_id(id)
        if not member:
            return {"error": "Member not found"}, 404

        if MemberRepository.find_by_email_or_phone(data['email'], data['phone']):
            return {"error": "Email or Phone already exists"}, 400

        member.name = data.get('name', member.name)
        member.phone = data.get('phone', member.phone)
        member.email = data.get('email', member.email)
        
        MemberRepository.update_member()
        return member.to_dict(), 200

    @staticmethod
    def delete_member(id):
        member = MemberRepository.get_member_by_id(id)
        if not member:
            return {"error": "Member not found"}, 404
        MemberRepository.delete_member(member)
        return {"message": f"Member with id {id} has been deleted."}, 200
