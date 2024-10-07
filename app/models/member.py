from app import db
from faker import Faker

fake = Faker()

class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "role": self.role
        }

    @classmethod
    def generate_fake_data(cls):
        """Generates a single fake Member instance."""
        return cls(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            role=fake.random_element(elements=("member", "admin"))
        )
