#user login database
class Login(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)