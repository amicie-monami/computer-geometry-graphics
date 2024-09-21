from window import Window
from tasker import Tasker 

class App:

    def __init__(self):
        self.window = Window(640, 480)
        self.tasker = Tasker(self.window)
        return
        
    def run(self):        
        window = self.window
        while not window.should_close():
            window.poll_events()
            self.tasker.handle_input()
            self.draw()

    def draw(self):
        self.window.clear()
        for obj in self.tasker.actual_objects():
            obj.draw()
        self.window.swap_buffers()

App().run()