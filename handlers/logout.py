#handler for logout
class LogoutHandler(Handler):
    def get(self):
        #delete cookie and redirect to signup page
        self.response.headers.add_header('Set-Cookie', str('name=%s; Path=/' % ""))        
        self.redirect('/signup')