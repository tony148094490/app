import webapp2

form="""
<form action="/rot13" method="post">
    <textarea name="text"  > this is called textarea </textarea>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
	self.response.headers['Content-Type'] = 'html'
	self.response.write(form)


class Rot13Handler(webapp2.RequestHandler):
    def post(self):
        inputString = self.request.get("text")

# do something craaazy here - or some sane algorithm
        

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(inputString)

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/rot13',Rot13Handler),
], debug=True)

