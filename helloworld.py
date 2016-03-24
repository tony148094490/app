import webapp2

form="""
<form action="/rot13" method="post">
    <textarea name="text">%(inputString)s</textarea>
    <input type="submit">
</form>
"""

class Rot13Handler(webapp2.RequestHandler):
    
    global alphabet
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def write_form(self, inputString=""):
        self.response.write(form % {"inputString": inputString})


    def rotate(self, inputString):
        if inputString == '':
            return inputString

        inputString = inputString.lower()
        result = ''
        for character in inputString:
            currentPosition = ord('z') - ord(character)
            newPosition = currentPosition + 13
            result = result + alphabet[(newPosition)%26]
        return result    

    def get(self):
        self.response.headers['Content-Type'] = 'html'
        self.write_form("Yeah right")

    def post(self):
        inputString = self.request.get("text")

        punctuation_character = ['.', '!', '?']

        list1 = ''
        tempString = ''

        for character in inputString:
            character = character.lower()
            if character in alphabet:
                tempString += character
            else:
                list1 += (self.rotate(tempString))
                list1 += character
                tempString = ''

        self.write_form(list1)



app = webapp2.WSGIApplication([
    ('/rot13',Rot13Handler),
], debug=True)