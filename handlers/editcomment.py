#handler for editing comments
class EditCommentHandler(Handler):
    def get(self, comment_id):
        #get username from cookie
        username = self.get_username()
        #if user is not logged in, redirect to login page
        if username == None:
            self.redirect("/login")
        else:
            #query comment from database
            co = Comment.get_by_id(int(comment_id))
            #check if user created this comment
            if co.username == username:
                #if true, render the edit comment page
                self.render("editcomment.html", 
                            content=co.content.replace('<br>', '\n'), 
                            error="", post_id = co.subject_id)
            else:
                self.redirect("/%s"%co.subject_id)

    def post(self, comment_id):
        #query the comment from database
        co = Comment.get_by_id(int(comment_id))
        #get the comment from user entry
        content = self.request.get("content")
        #if user enters content, update the comment in database
        if content:
            co.content = content.replace('\n', '<br>')
            co.put()
            #time.sleep(0.5)
            self.redirect("/%s"%co.subject_id)
        else:
            #if no content, print error
            error = "content please!"
            self.render("editcomment.html",  
                        content = content, error = error, 
                        post_id = co.subject_id)
