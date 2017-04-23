#handler for signup page
class SignupHandler(Handler):
    def get(self):
        #render the signup page
        self.render("user.html", error_username="", error_password="", 
                    error_verify="", error_email="")
    
    def post(self):
        #get user entries
        username = self.request.get("username")
        password1 = self.request.get("password")
        password2 = self.request.get("verify")
        email = self.request.get("email")
        
        #verify entries
        error_username = self.check_username(username)
        error_password, error_verify = self.check_password(password1, password2)
        error_email = self.check_email(email)
        #if no error, create cookie and store login in the database, then redirect to login page
        if error_username == "" and error_password == "" and error_verify == "" and error_email == "":
            new_cookie_val = make_secure_val(username)
            self.response.headers.add_header('Set-Cookie', str('name=%s; Path=/' % new_cookie_val))
            a = Login(username=username, password=make_pw_hash(username, password1))
            a.put()
            self.redirect('/welcome')
        #otherwise, render the page with errors
        else:
            self.render("user.html", error_username = error_username, 
                        error_password = error_password, 
                        error_verify = error_verify, 
                        error_email = error_email, 
                        username = username, email = email)

    def check_username(self, username):
        #check if username follows the required pattern
        check = u_re.match(username)
        #query the username in the database
        login = db.GqlQuery("select * from Login where username = '%s'"%username)
        #check if username exists in database
        count = 0
        for i in login:
            count += 1
            break
        #if username is invalid, print error
        if check == None:
            return "That's not a valid username."
        #error when username already exists
        elif count == 1:
            return "Username already exists!"
        else:
            return ""

    def check_password(self, password1, password2):
        #check if password fits into pattern
        check = p_re.match(password1)
        if check == None:
            return "That wasn't a valid password.", ""
        #check is password matches
        elif password1 != password2:
            return "", "Your passwords didn't match."
        else:
            return "", ""

    def check_email(self, email):
        #check if email follows the pattern
        check = e_re.match(email)
        #if email follows the pattern or left blank, return no error
        if check != None or email == "":
            return ""
        else:
            return "That's not a valid email."
            