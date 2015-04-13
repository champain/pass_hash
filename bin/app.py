import web
import crypt
from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = "/home/jacob/pass_hasher/secret/server.crt"
CherryPyWSGIServer.ssl_private_key = "/home/jacob/pass_hasher/secret/server.key"

db = web.database(dbn="postgres", db="passhash", user="passhash", pw="urdadallday")
t = db.transaction()
urls = (
        '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class Index(object):
    def GET(self):
        return render.passhash() 
    
    def POST(self):
        form = web.input()
        passw =  crypt.crypt(form.passw, '$1$/Bhh.EhJkjj$')
        pass_check = crypt.crypt(form.passwcheck, '$1$/Bhh.EhJkjj$')
        if  passw == pass_check:
            content = "Passwords match."
            try:
                db.insert('hashes', title=passw)
            except:
                t.rollback()
                raise
            else:
                t.commit()
        else:
            content = "Passwords don't match. Please press your back button and try again."
        return render.index(content = content)

if __name__ == "__main__":
    app.run()
