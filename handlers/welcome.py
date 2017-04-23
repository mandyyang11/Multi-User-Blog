#handler for welcome page
class WelcomeHandler(Handler):
    def get(self):
        #get name from cookie
        name = self.get_username()
        #check if there is correct cookie, if true, render the welcome page
        if name != None:
            self.render("welcome.html", name=name)
        #otherwise, redirect to signup page
        else:
            self.redirect('/signup')