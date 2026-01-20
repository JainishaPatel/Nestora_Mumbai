from models import db_connection
from models import User
from datetime import datetime


# ---------------- INSERT NEW USER ----------------
def insert_user(user):
    """
    Inserts a new user into the users table.
    """
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO users(
        user_id, name, email, password_hash, phone,
        last_login, is_active, is_admin
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        user.user_id,
        user.name,
        user.email,
        user.password_hash,
        user.phone,
        user.last_login,
        user.is_active,
        int(getattr(user, "is_admin", 0))  # default 0
    )

    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


# ---------------- GET USER BY EMAIL ----------------
def get_user_by_email(email):
    """
    Fetches a user by email.
    Returns a User object if found, else None.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row:
        return User(
            user_id=row.get("user_id"),
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            phone=row["phone"],
            created_on=row.get("created_on"),
            last_login=row.get("last_login"),
            is_active=row.get("is_active", True),
            is_admin=row.get("is_admin", 0)
        )
    return None


# ---------------- UPDATE LAST LOGIN ----------------
def update_last_login(user_id):
    """
    Updates the last_login timestamp for the user.
    """
    db = db_connection()
    cursor = db.cursor()
    sql = "UPDATE users SET last_login = %s WHERE user_id = %s"
    cursor.execute(sql, (datetime.now(), user_id))
    db.commit()
    cursor.close()
    db.close()


# ---------------- GET USER PROFILE ----------------
def user_profile(user_id):
    """
    Fetch basic profile info for a user.
    Returns dictionary with name, email, phone, created_on, last_login.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT name, email, phone, created_on, last_login FROM users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    user_info = cursor.fetchone()

    cursor.close()
    db.close()
    return user_info


# ---------------- UPDATE USER PROFILE ----------------
def update_user_profile(user_id, name, phone):
    """
    Update user's name and phone.
    """
    db = db_connection()
    cursor = db.cursor()

    sql = "UPDATE users SET name = %s, phone = %s WHERE user_id = %s"
    cursor.execute(sql, (name, phone, user_id))
    db.commit()
    cursor.close()
    db.close()


# ---------------- UPDATE USER PASSWORD ----------------
def update_user_password(user):
    """
    Update the password hash for a user.
    """
    db = db_connection()
    cursor = db.cursor()
    sql = "UPDATE users SET password_hash=%s WHERE user_id=%s"
    cursor.execute(sql, (user.password_hash, user.user_id))
    db.commit()
    cursor.close()
    db.close()
    

# ---------------- SAVE PASSWORD RESET TOKEN ----------------
def save_reset_token(user_id, token, expires):
    """
    Save a password reset token and expiry datetime for a user.
    """
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users
        SET reset_token = %s, reset_expires = %s
        WHERE user_id = %s
    """, (token, expires, user_id))
    db.commit()
    cursor.close()
    db.close()


# ---------------- GET USER BY RESET TOKEN ----------------
def get_user_by_reset_token(token):
    """
    Fetch a user by reset token if token is still valid (not expired).
    Returns a User object if valid, else None.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM users
        WHERE reset_token = %s
          AND reset_expires > NOW()
    """, (token,))
    row = cursor.fetchone()
    cursor.close()
    db.close()

    return User(**row) if row else None


# ---------------- CLEAR PASSWORD RESET TOKEN ----------------
def clear_reset_token(user_id):
    """
    Clear a user's reset token and expiry after password reset.
    """
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users
        SET reset_token = NULL, reset_expires = NULL
        WHERE user_id = %s
    """, (user_id,))
    db.commit()
    cursor.close()
    db.close()



# #---------------- GET USER BY ID (OPTIONAL / COMMENTED) ----------------
# def get_user_by_email_by_id(user_id):
#     """
#     Fetch a user by user_id.
#     Returns a User object if found, else None.
#     """
#     db = db_connection()
#     cursor = db.cursor(dictionary=True)
#     sql = "SELECT * FROM users WHERE user_id=%s"
#     cursor.execute(sql, (user_id,))
#     row = cursor.fetchone()
#     cursor.close()
#     db.close()
#     if row:
#         return User(
#             user_id=row["user_id"],
#             name=row["name"],
#             email=row["email"],
#             password_hash=row["password_hash"],
#             phone=row.get("phone"),
#             created_on=row.get("created_on"),
#             last_login=row.get("last_login"),
#             is_active=row.get("is_active", True)
#         )
#     return None

