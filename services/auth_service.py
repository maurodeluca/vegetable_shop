from models.user import User

class AuthService:
    def verify_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
