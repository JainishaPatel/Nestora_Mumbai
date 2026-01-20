from dotenv import load_dotenv
load_dotenv()

from data import properties, users
from models import insert_property, insert_user

def seed_data():
    for user in users:
        insert_user(user)

    for prop in properties:
        insert_property(prop)

    print("[DEV] Users and properties seeded successfully")

if __name__ == "__main__":
    seed_data()
