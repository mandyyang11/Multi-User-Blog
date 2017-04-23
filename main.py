#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#import libraries
import jinja2
import webapp2
import os
import re
import hmac
import random
import string
import hashlib
import time
from google.appengine.ext import db

#import models
from models/user.py import *
from models/post.py import *
from models/omment.py import *

#import handlers
from handlers/main.py import *
from handlers/signup.py import *
from handlers/login.py import *
from handlers/logout.py import *
from handlers/welcome.py import *
from handlers/newpost.py import *
from handlers/post.py import *
from handlers/like.py import *
from handlers/edit.py import *
from handlers/delete.py import *
from handlers/comment.py import *
from handlers/editcomment.py import *
from handlers/deletecomment.py import *

#set a secret string for cookie
secret = "asdfgh"

#helper functions for hashing cookies
def hash_str(s):
	return hmac.new(secret, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" %(s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val	

#helper functions for hashing passwords
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    ha, salt = h.split(",")
    ha2 =  hashlib.sha256(name + pw + salt).hexdigest()
    if ha == ha2:
        return True
    else:
        return False

#setting up jinja2 environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape=True)

#regular expressions for pattern matching
u_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
p_re = re.compile(r"^.{3,20}$")
e_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

#default Handler class 
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    #check if user is logged in  
    def login_check(self):
        name = None
        name_cookie_str = self.request.cookies.get('name')
        if name_cookie_str:
            cookie_val = check_secure_val(name_cookie_str)
            if cookie_val:
                name = cookie_val
        if name != None:
            return "%s (<a class=\"login-link\" href=\"/logout\">Logout</a>)"%name
        else:
            return """<a class="login-link" href="/login">Login</a>
            |
            <a class="login-link" href="/signup">Signup</a>"""
    
    #getting username
    def get_username(self):
        name = None
        name_cookie_str = self.request.cookies.get('name')
        if name_cookie_str:
            cookie_val = check_secure_val(name_cookie_str)
            if cookie_val:
                name = cookie_val
        return name


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/newpost', NewpostHandler),
                               ('/(\d+)', PostHandler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler), 
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/like/(\d+)', LikeHandler),
                               ('/edit(\d+)', EditHandler),
                               ('/delete(\d+)', DeleteHandler),
                               ('/comment(\d+)', CommentHandler),
                               ('/editComment(\d+)', EditCommentHandler),
                               ('/deleteComment(\d+)', DeleteCommentHandler)
                               ], debug=True)
