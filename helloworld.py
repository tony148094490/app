import webapp2

form="""
<form action="/rot13" method="post">
    <textarea rows="20" cols="50" name="text">%(inputString)s</textarea>
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
                currentPosition = ord(character) - ord('A')
                newPosition = currentPosition + 13
                result = result + alphabetUpper[(newPosition)%26]

            else:
                currentPosition = ord(character) - ord('a')
                newPosition = currentPosition + 13
                result = result + alphabetLower[(newPosition)%26]


        return result    

    def doEscape(self, s):
        esc = (("&", "&amp;"),
               (">", "&gt;"),
               ("<", "&lt;"),
               ('"', "&quot;"))
           
        for (i,o) in esc:
            s = s.replace(i,o)
        return s

    def get(self):
        self.response.headers['Content-Type'] = 'html'
        self.write_form("We are going to rot 13!")

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

        # if we still have some things to rotate - last char is valid
        if tempString != '':
            # a valid word 
            if len(tempString) > 1 or (len(tempString) == 1 and (tempString in alphabetLower or tempString in alphabetUpper)):
                list1 += (self.rotate(tempString))
            # a special character that does not need rotation
            else:
                list1 += tempString

        # escape before writing

        list1 = self.doEscape(list1)

        self.write_form(list1)

app = webapp2.WSGIApplication([
    ('/rot13',Rot13Handler),
], debug=True)