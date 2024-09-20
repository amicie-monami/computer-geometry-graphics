from OpenGL.GL import * 
import window
from triangle import Triangle
import numpy as np

class App:

    def __init__(self):
        self.window = window.Window() 
        self.create_triangles()
        self.main_loop()
        return
        
    def main_loop(self):
        while not self.window.should_close():
            self.window.clear()

            for triangle in self.triangles:
                triangle.draw()

            self.window.poll_events()
            self.window.swap_buffers()
        return
    
    def create_triangles(self):
        self.triangles = [
            Triangle(
                np.array([
                    -0.9, -0.5, 0.0,
                    -0.5, -0.5, 0.0,
                    -0.7,  0.5, 0.0 
                ], np.float32), 
                "shaders/vertex.glsl", 
                "shaders/fragment_left.glsl",
            ),
            Triangle(
                np.array([
                    -0.4,  0.5, 0.0,
                     0.4,  0.5, 0.0,
                     0.0, -0.5, 0.0 
                ], np.float32), 
                "shaders/vertex.glsl", 
                "shaders/fragment_center.glsl",
            ),
            Triangle(
                np.array([
                    0.9, -0.5, 0.0,
                    0.5, -0.5, 0.0,
                    0.7,  0.5, 0.0 
                ], np.float32), 
                "shaders/vertex.glsl", 
                "shaders/fragment_right.glsl",
            ),
        ]
        return
App()