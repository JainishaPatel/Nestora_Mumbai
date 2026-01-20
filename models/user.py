from datetime import datetime, timedelta
import bcrypt
import secrets

class User:
    def __init__(
        self,
        user_id,
        name,
        email,
        password=None,
        password_hash=None,
        phone=None,
        created_on=None,
        last_login=None,
        is_active=True,
        is_admin=False,  
        reset_token=None,
        reset_expires=None
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_on = created_on
        self.last_login = last_login
        self.is_active = is_active
        self.is_admin = bool(is_admin)
        self.reset_token = reset_token
        self.reset_expires = reset_expires

        # Handle password
        if password:
            self.set_password(password)
        elif password_hash:
            self.password_hash = password_hash
        else:
            self.password_hash = None

        # For password reset
        self.reset_token = None
        self.reset_expires = None


    # ---------------- Password handling ----------------
    def set_password(self, password):
        """Hashes and stores the password securely."""
        password_bytes = password.encode("utf-8")
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        self.password_hash = hashed.decode("utf-8")

    def check_password(self, password):
        """Checks a password against the stored hash."""
        if not self.password_hash:
            return False
        password_bytes = password.encode("utf-8")
        stored_hash = self.password_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, stored_hash)

   
    # ---------------- Login tracking ----------------
    def update_last_login(self):
        """Updates the last login timestamp."""
        self.last_login = datetime.now()

  
    # ---------------- Password reset ----------------
    def generate_reset_token(self, expiry_hours=1):
        """Generates a secure password reset token with expiration."""
        token = secrets.token_urlsafe(32)
        self.reset_token = token
        self.reset_expires = datetime.now() + timedelta(hours=expiry_hours)
        return token

    def validate_reset_token(self, token):
        """Validates a reset token."""
        if self.reset_token != token:
            return False
        if datetime.now() > self.reset_expires:
            return False
        return True

    def clear_reset_token(self):
        """Clears the reset token after successful password reset."""
        self.reset_token = None
        self.reset_expires = None

   
    # ---------------- Utility ----------------
    def deactivate(self):
        """Soft deactivate the user."""
        self.is_active = False

    def activate(self):
        """Activate a previously deactivated user."""
        self.is_active = True
