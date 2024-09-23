import glfw
from OpenGL.GL import *

from shader import Shader
import shapes.figure as figure
from window import SCREEN_WIDTH, SCREEN_HEIGHT

SCALE_X = SCREEN_HEIGHT / SCREEN_WIDTH
SCALE_Y = 1.0

class Tasker:

    def __init__(self, window):
        self.objects = []
        self.window = window
        
        self.last_task = self.first_task
        self.paragraph = glfw.KEY_A

        self.tasks_keys = [glfw.KEY_1]
        tasks_handlers  = [self.first_task]
        self.tasks = {key: task for key, task in zip(self.tasks_keys, tasks_handlers)}
        
        self.shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        glfw.set_key_callback(window.window, self.handle_input)


    def render_objects(self):
        """
        Rendering of the current scene
        """
        for object in self.objects:
            object.draw()


    def handle_input(self, window, key, scancode, action, mods):
        """
        Proccesses keyboard input and
        switches between tasks 
        """

        for key in self.tasks_keys:
            if self.window.get_key(key) == glfw.PRESS:
                self.tasks[key]()


    def first_task(self):
        """
        Draw three flat figures with different depth coordinates z
        """
        triangle = figure.triangle(self.shader, vertices=[(0, 0.3, 0.2), (0.3, 0.3, 0), (0, 0, 0.7)])
        self.objects.append(triangle)

        rectangle = figure.rectangle(self.shader, [(-0.5, 0.5, 0.3),(-0.5, -0.5, 0.3),(0.5, -0.5, 0.3), (0.5, 0.5, 0.3)])
        self.objects.append(rectangle)
        
        triangle = figure.triangle(self.shader, vertices=[(0, 0.3, 0.2), (0.3, 0.3, 0), (0, 0, 0.7)])
        self.objects.append(triangle)
        self.last_task = self.first_task
