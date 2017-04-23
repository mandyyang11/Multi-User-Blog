#blog post database
class Blog(db.Model):
    username = db.StringProperty(required = True)
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    likes = db.IntegerProperty(required = True)
    liked_users = db.ListProperty(str ,required = True)