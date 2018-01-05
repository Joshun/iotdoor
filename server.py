import tornado.ioloop
import tornado.web
from tornado import template
from datetime import datetime
# import time


class ViewHandler(tornado.web.RequestHandler):
    def initialize(self, door_state):
        self.door_state = door_state
    def get(self):
        loader = template.Loader("templates")
        print(door_state.was_rung())
        page = loader.load("home.html").generate(was_rung=self.door_state.was_rung())
        self.write(page)

class DoorHandler(tornado.web.RequestHandler):
    def initialize(self, door_state):
        self.door_state = door_state
    def get(self):
        self.write("request received")
        self.door_state.ring()

class DoorState:
    def __init__(self):
        self.last_ring_time = None

    def ring(self):
        self.last_ring_time = datetime.now()
    
    def was_rung(self):
        if self.last_ring_time is None:
            return False
        else:
            current_time = datetime.now()
            timediff = (current_time - self.last_ring_time)
            timediff_secs = (timediff.days*60*60*24) + (timediff.seconds) + (timediff.seconds)
            return timediff_secs < 5*60
        


def make_app(door_state):
    return tornado.web.Application([
        (r"/", ViewHandler, {"door_state": door_state}),
        (r"/door", DoorHandler, {"door_state": door_state}),
    ], debug=True)

if __name__ == "__main__":
    door_state = DoorState()
    app = make_app(door_state)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
