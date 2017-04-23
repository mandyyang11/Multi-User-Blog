#Handler for liking a post
class LikeHandler(Handler):
    def get(self, post_id):
        #get username from cookie
        username = self.get_username()
        #if the user is not logged in, redirect to login page
        if username == None:
            self.redirect("/login")
        else:
            #query the post from the database
            po = Blog.get_by_id(int(post_id))
            #check if the user ever liked the page
            if username not in po.liked_users:        
                #likes increment by one
                po.likes += 1
                #add username to liked_users
                po.liked_users.append(username)
                #update the post in the database
                po.put()
            self.redirect("/%s"%post_id)