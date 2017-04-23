#Handler for adding new post
class NewpostHandler(MainHandler):
    def get(self):
        #getting username from cookie
        name = self.get_username()
        #if user is logged in, render the new post page. otherwise, redirect to login page.
        if name != None:
            self.render("blog.html", subject="", content="", error="")
        else:
            self.redirect("/login")

    def post(self):
        #get subject and content from user entry
        username = self.get_username()
        subject = self.request.get("subject")
        content = self.request.get("content")
        likes = 0
        liked_users = [username]
        #if user enter both subject and content, create a new blog post and store in database
        if subject and content:
            a = Blog(username = username, subject = subject, 
                     content = content.replace('\n', '<br>'),
                     likes = likes, liked_users = liked_users)
            a.put()
            #redirect to new post
            self.redirect("/%s"%a.key().id())
        else:
            #if either subject or content is missing, print the error messege on bottom
            error = "subject and content please!"
            self.render("blog.html", subject = subject, 
                        content = content, error = error) 
            