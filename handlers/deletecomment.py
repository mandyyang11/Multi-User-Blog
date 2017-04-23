#handler for deleting comment
class DeleteCommentHandler(Handler):
    def get(self, comment_id):
        #get user from cookie
        username = self.get_username()
        #query comment from database
        co = Comment.get_by_id(int(comment_id))
        #if user is not logged in, redirect to login page
        if username == None:
            self.redirect("/login")
        #if user created this comment, delete the comment from database
        elif co.username == username:
            co.delete()
            #time.sleep(0.5)
            self.redirect('/%s'%co.subject_id)
        else:
            self.redirect('/%s'%co.subject_id)