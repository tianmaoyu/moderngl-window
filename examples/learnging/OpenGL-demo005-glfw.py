import glfw
from OpenGL.GL import *


def run() -> None:
    if not glfw.init():
        print("初始化GLFW错误！")
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(600, 400, "005",None,None)
    glfw.set_window_pos(window, 100, 100)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glClearNamedFramebufferfv(0, GL_COLOR, 0, (0.8, 0.8, 0.8, 1.0))

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    run()
