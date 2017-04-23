#comment database
class Comment(db.Model):
    username = db.StringProperty(required = True)
    subject_id = db.IntegerProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)