#handler for adding new comment
class CommentHandler(Handler):
    def get(self, post_id):
        #get username from cookie
        username = self.get_username()
        #get post from database
        po = Blog.get_by_id(int(post_id))
        #if user is not logged in, redirect to login page
        if username == None:
            self.redirect("/login")
        #otherwise, render the new comment page
        else:
            self.render('newcomment.html', content = "", 
                        post_id=post_id, error = "")

    def post(self, post_id):
        #get username from cookie
        username = self.get_username()
        #get content from user entry
        content = self.request.get("content")
        #if user enters some content, create the comment and store into the database
        if content:
            a = Comment(username = username, subject_id = int(post_id), 
                        content = content.replace('\n', '<br>'))
            a.put()
            #time.sleep(0.5)
            self.redirect("/%s"%post_id)
        else:
            #if no content, it will show error
            error = "content please!"
            self.render("newcomment.html", content = content, 
                        post_id = post_id, error = error) 
            