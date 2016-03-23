import webapp2

form="""
<form action="/rot13" method="post">
    <textarea name="text"  > this is called textarea </textarea>
    <input type="submit">
</form>
"""

class Rot13Handler(webapp2.RequestHandler):
    
    global alphabet
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def rotate(self, inputString):
        if inputString == '':
            return inputString

        inputString = inputString.lower()
        result = ''
        for character in inputString:
            result = result + alphabet[(character + 13)%26]
        return result    

    def get(self):
        self.response.headers['Content-Type'] = 'html'
        self.response.write(form)

    def post(self):
        inputString = self.request.get("text")

        punctuation_character = ['.', '!', '?']

        list1 = []
        tempString = ''

        for character in inputString:
            character = character.lower()
            if character in alphabet:
                tempString += character
            else:
                list1.append(self.rotate(tempString))
                list1.append(character)
                tempString = ''

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(list1)




app = webapp2.WSGIApplication([
    ('/rot13',Rot13Handler),
], debug=True)

