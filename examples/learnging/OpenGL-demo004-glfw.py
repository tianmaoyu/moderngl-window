import glfw
from OpenGL.GL import *

glfw.init()
window = glfw.create_window(800, 600, "glfw first", None, None)
glfw.make_context_current(window)

while not glfw.window_should_close(window):

    glClearColor(1.0, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glfw.swap_buffers(window)
    glfw.poll_events()

# glfw.destroy_window(window)
# glfw.terminate()