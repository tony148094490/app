import webapp2

form="""
<form action="/rot13" method="post">
    <textarea name="text">%(inputString)s</textarea>
    <input type="submit">
</form>
"""

class Rot13Handler(webapp2.RequestHandler):
    
    global alphabetLower
    alphabetLower = 'abcdefghijklmnopqrstuvwxyz'
    global alphabetUpper
    alphabetUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def write_form(self, inputString=""):
        self.response.write(form % {"inputString": inputString})

    def rotate(self, inputString):
        if inputString == '':
            return inputString

        result = ''
        
        for character in inputString:
            isUpperCase = (ord(character) - ord('a'))
            if(isUpperCase < 0):
                currentPosition = ord('Z') - ord(character)
                newPosition = currentPosition + 13
                result = result + alphabetUpper[(newPosition)%26]

            else:
                currentPosition = ord('z') - ord(character)
                newPosition = currentPosition + 13
                result = result + alphabetLower[(newPosition)%26]


        return result    

    def get(self):
        self.response.headers['Content-Type'] = 'html'
        self.write_form("This form will rotate your character to the right 13 times!")

    def post(self):
        inputString = self.request.get("text")

        punctuation_character = ['.', '!', '?']

        list1 = ''
        tempString = ''

        for character in inputString:
            if character in alphabetLower or character in alphabetUpper:
                tempString += character
            else:
                list1 += (self.rotate(tempString))
                list1 += character
                tempString = ''

        if tempString != '':
            if len(tempString) > 1 or (len(tempString) == 1 and (tempString in alphabetLower or tempString in alphabetUpper)):
                list1 += (self.rotate(tempString))
            else:
                list1 += tempString

        self.write_form(list1)

app = webapp2.WSGIApplication([
    ('/rot13',Rot13Handler),
], debug=True)