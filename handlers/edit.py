#Handeler to edit blog posts
class EditHandler(Handler):
    def get(self, post_id):
        #get username from cookie
        username = self.get_username()
        #if user is not logged in, redirect to login page
        if username == None:
            self.redirect("/login")
        else:
            #query the post
            po = Blog.get_by_id(int(post_id))
            #render the post edit page if user created the post
            if po.username == username:
                self.render("editpost.html", subject=po.subject, 
                            content=po.content.replace('<br>', '\n'), 
                            error="", post_id = po.key().id())
            else:
                self.redirect("/%s"%post_id)

    def post(self, post_id):
        #get the post from database
        po = Blog.get_by_id(int(post_id))
        #get the subject and content from user entry
        subject = self.request.get("subject")
        content = self.request.get("content")
        #if subject and content exists, update the subject and the content for the post
        if subject and content:
            po.subject = subject
            po.content = content.replace('\n', '<br>')
            po.put()
            self.redirect("/%s"%po.key().id())
        else:
            #otherwise, print error on the page
            error = "subject and content please!"
            self.render("editpost.html", subject = subject, 
                        content = content, error = error, 
                        post_id = po.key().id())
            