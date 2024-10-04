from faker import Faker
from models import db, Member  
from app import create_app  


fake = Faker()

def seed_members(count=10):
    """Seeds the database with fake Member data."""
    for _ in range(count):
        member = Member.generate_fake_data()
        db.session.add(member)
    db.session.commit()  

if __name__ == '__main__':
    app = create_app()  
    with app.app_context():
    
        db.create_all()  

        seed_members(10) 

    print("Database seeded with fake member data.")
