import os
import datetime
import jinja2
import webapp2
import re

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

# class Post(ndb.Model):
# 	subject = ndb.StringProperty(required = True)
# 	content = ndb.TextProperty(required = True)
# 	createdDate = ndb.DateProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class SignUpPageHandler(Handler):
	def get(self):
		self.render("signup.html",
					username="",
					password="",
					verify="",
					email="",
					usernameError="",
					passwordError="",
					verifyError="",
					emailError="")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		
		usernameError = ""
		passwordError = ""
		verifyError = ""
		emailError = ""
		
		if ( (self.validUserName(username)) and self.validPassword(password) and self.validVerification(password, verify) and self.validEmail(email) ):
			self.response.headers.add_header('Set-Cookie', 'username=%s' % str(username))
			self.redirect("/welcome")
		else: 
			if(not self.validUserName(username)):
				usernameError = "That's not a valid username."
			if(not self.validPassword(password)):
				passwordError = "That wasn't a valid password."
				password = ""
				verify = ""
			if(self.validPassword(password) and not self.validVerification(password, verify)):
				verifyError = "Your passwords didn't match."
				password = ""
				verify = ""
			if(not self.validEmail(email)):
				emailError = "That's not a valid email."

			self.render("signup.html",
						username = username,
						password = password,
						verify = verify,
						email = email,
						usernameError = usernameError,
						passwordError = passwordError,
						verifyError = verifyError,
						emailError = emailError)

		
	def validUserName(self, user_name):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return USER_RE.match(user_name)

	def validPassword(self, pswd):
		PSWD_RE = re.compile(r"^.{3,20}$")
		return PSWD_RE.match(pswd)

	def validVerification(self, first, second):
		return first == second

	def validEmail(self, email):
		if email == "":
			return True
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		return EMAIL_RE.match(email)	

class WelcomeHandler(Handler):
	def get(self):
		cookieUsername = self.request.cookies.get("username")
		username = self.decryptCookie(cookieUsername)
		if (isValidUser(username)):
			self.response.write("Welcome, " + username + "!")
		else:
			self.redirect('signup')

	def decryptCookie(self, cookie):

	def isValidUser(self, username):


app = webapp2.WSGIApplication([('/signup', SignUpPageHandler),
							   ('/welcome', WelcomeHandler),
							  ],
								debug=True)