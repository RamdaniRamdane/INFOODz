def check_login(email, password):
    from website import bcrypt 
    from .models import User
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    else:
        return False
    

