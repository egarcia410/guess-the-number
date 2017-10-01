import os

import random
import tornado.ioloop
import tornado.web

from jinja2 import Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8888'))

ENV = Environment(
    loader=PackageLoader('guessGame'),
    autoescape=select_autoescape(['html', 'xml'])
)

class SecretNum():
    def __init__(self, difficulty=None):
        self.difficulty = difficulty
        self.secretNum = 0
        if difficulty == 'Easy':
            self.secretNum = random.randint(1, 51)
        elif difficulty == 'Medium':
            self.secretNum = random.randint(1, 101)
        elif difficulty == 'Hard':
            self.secretNum = random.randint(1, 501)

    def getSecretNum(self):
        return self.secretNum

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context={}):
        template = ENV.get_template(tpl)
        self.write(template.render(context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("index.html")

    def post(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        difficulty = self.get_body_argument('difficulty')
        SecretNum(difficulty)
        self.render_template("play.html")

class PlayHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("play.html")

    def post(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        number = self.get_body_argument('number')
        if number == "":
            print('empty string')
            return self.render_template("play.html")        
        content = ""
        number = int(number)
        print(SecretNum().getSecretNum())
        if number == SecretNum().getSecretNum():
            content = "You Guessed Correctly!"
        elif number < SecretNum().getSecretNum():
            content = 'Guess Higher'
        elif number > SecretNum().getSecretNum():
            content = 'Guess Lower'
        self.render_template("play.html", {'content': content, 'number': number})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/play", PlayHandler),
        (
        r"/static/(.*)",
        tornado.web.StaticFileHandler,
        {'path': 'static'}
        )
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('Creating magic on port {}'.format(PORT)))
    tornado.ioloop.IOLoop.current().start()
