from models import User
from datetime import datetime
import uuid
import os


# ---------------- ADMIN USER ----------------
admin = User(
    user_id=str(uuid.uuid4()),
    name=os.getenv("ADMIN_NAME", "Admin"),
    email=os.getenv("ADMIN_EMAIL"),
    phone=os.getenv("ADMIN_PHONE"),
    created_on=datetime.now(),
    is_active=True
)
admin.is_admin = True
admin.set_password(os.getenv("ADMIN_PASSWORD"))


# ---------------- NORMAL USERS (FAKE) ----------------
def fake_user(name, email, password="password123", active=True):
    """
    Creates a fake user with a fixed password.
    """
    user = User(
        user_id=str(uuid.uuid4()),
        name=name,
        email=email,
        phone=str(uuid.uuid4().int)[:10],
        created_on=datetime.now(),
        is_active=active
    )
    user.set_password(password)
    # print(f"[DEV] User: {email} | Password: {password}")
    return user

# Create fake users with visible passwords
u1 = fake_user("Jack", "jack@test.com", password="Jack@2026$Dev")
u2 = fake_user("Jenny", "jenny@test.com", password="Jenny@2026$Dev")
u3 = fake_user("John", "john@test.com", password="John@2026$Dev", active=False)

# ---------------- INSERT INTO DB ----------------
users = [admin, u1, u2, u3]
