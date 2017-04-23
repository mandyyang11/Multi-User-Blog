#Handler for the main page
class MainHandler(Handler):
    def render_blog(self, subject="", content="", error=""):
        #query every blog post in the database
        blogs = db.GqlQuery("select * from Blog order by created desc")
        #checking if user is logged in. if logged in, display new post option on bottom. 
        if self.get_username() != None:
            new_post = 'New Post'
        else:
            new_post = ''
        self.render("display.html", loginCheck=self.login_check(), 
                    blogs=blogs, new_post = new_post)
    
    def get(self):
        self.render_blog()