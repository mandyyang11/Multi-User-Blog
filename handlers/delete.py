#handler for deleting blog posts
class DeleteHandler(Handler):
    def get(self, post_id):
        #get username from cookie
        username = self.get_username()
        #query the blog post from the database
        po = Blog.get_by_id(int(post_id))
        #if user is not logged in, redirect to user page
        if username == None:
            self.redirect("/login")
        #if the user created this post, delete the post
        elif po.username == username:
            po.delete()
            self.redirect('/%s'%post_id)
        else:
            self.redirect('/%s'%post_id)
            