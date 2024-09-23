from window import Window
from tasker import Tasker 

class App:

    def __init__(self):
        self.window = Window()
        self.tasker = Tasker(self.window)
        return
        
    def run(self):        
        window = self.window
        while not window.should_close():
            window.poll_events()
            self.draw()

    def draw(self):
        self.window.clear()
        self.tasker.render_objects()
        self.window.swap_buffers()

App().run()