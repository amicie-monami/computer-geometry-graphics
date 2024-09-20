import glfw
from OpenGL.GL import *
import atexit

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Window:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        glfw.init()
        self.window = glfw.create_window(width, height, "First Practice", None, None)
        glfw.make_context_current(self.window)
        glClearColor(0.1, 0.2, 0.2, 1)
        atexit.register(self.__terminate__)

    def poll_events(self):
        glfw.poll_events()
        if self.get_key(glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def get_key(self, key):
        return glfw.get_key(self.window, key)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.set_window_should_close(self.window, True)

    def __terminate__(self):
        glfw.destroy_window(self.window)
        glfw.terminate()