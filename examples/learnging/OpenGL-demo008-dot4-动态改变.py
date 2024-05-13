import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import math

# 初始化GLFW
if not glfw.init():
    raise Exception("GLFW初始化失败")

# 创建窗口
window = glfw.create_window(800, 600, "OpenGL Color Change", None, None)
if not window:
    glfw.terminate()
    raise Exception("窗口创建失败")

glfw.make_context_current(window)

# 顶点数据
vertices = np.array([
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,  # 左下角，红色
    0.5, -0.5, 0.0, 0.0, 1.0, 0.0,  # 右下角，绿色
    0.0, 0.5, 0.0, 0.0, 0.0, 1.0  # 顶部，蓝色
], dtype=np.float32)

# 编译着色器
vertex_shader = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;
out vec3 ourColor;
void main()
{
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

fragment_shader = """
#version 330 core
out vec4 FragColor;
uniform vec4 ourColor;
void main()
{
    FragColor = ourColor;
}
"""

shader_program = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
                                compileShader(fragment_shader, GL_FRAGMENT_SHADER))

# 创建顶点缓冲对象和顶点数组对象
VBO = glGenBuffers(1)
VAO = glGenVertexArrays(1)

glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(1)

# 渲染循环
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)

    # 更新uniform颜色
    time_value = glfw.get_time()
    green_value = math.sin(time_value) / 2.0 + 0.5
    red_value = math.cos(time_value) / 2.0 + 0.5
    vertex_color_location = glGetUniformLocation(shader_program, "ourColor")
    glUniform4f(vertex_color_location, red_value, green_value, 0.0, 1.0)

    glBindVertexArray(VAO)
    glPointSize(20.0)
    glDrawArrays(GL_POINTS, 0, 3)

    glBindVertexArray(0)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
