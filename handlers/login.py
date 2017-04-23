#handler for login page
class LoginHandler(Handler):
    def get(self):
        #render login page
        self.render("login.html", error = "")

    def post(self):        
        #get username and password from user entry
        username = self.request.get("username")
        password = self.request.get("password")
        #query login from the database
        login = db.GqlQuery("select * from Login where username = '%s'"%username)
        for i in login:
            #check if username and password are valid
            if valid_pw(username, password, login[0].password):
                #set cookie and redirect to welcome
                new_cookie_val = make_secure_val(username)
                self.response.headers.add_header('Set-Cookie', str('name=%s; Path=/' % new_cookie_val))    
                self.redirect('/welcome')
        #otherwise render login page with error
        self.render("login.html", error = "Invalid login")