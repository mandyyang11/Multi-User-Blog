#Handler for displaying post with post_id
class PostHandler(Handler):
    def get(self, post_id):
        #query the post with post_id
        po = Blog.get_by_id(int(post_id))
        #if post exists, render the post page
        if po:
            d = po.created.strftime("%B %d, %Y")
            comments = db.GqlQuery("select * from Comment where subject_id = %s order by created"%post_id)
            self.render("blogpost.html", loginCheck = self.login_check(),
                        post_id = post_id, subject = po.subject, 
                        content = po.content, created = d, likes = po.likes,
                        username = po.username, comments = comments)
        #otherwise, redirect to main page
        else:
            self.redirect('/')