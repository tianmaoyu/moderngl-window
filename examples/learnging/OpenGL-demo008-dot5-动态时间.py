import numpy as np
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import time
import ctypes

glfw.init()
window = glfw.create_window(800, 600, "OpenGL VAO VBO Example", None, None)
glfw.make_context_current(window)

# 定义顶点着色器
vertex_shader = """  
#version 330 core  
layout (location = 0) in vec4 position;  
layout (location = 1) in vec4 color;  
out vec4 vertexColor;  
void main()  
{  
    gl_Position = position;  
    vertexColor = color;  
}  
"""

# 定义片段着色器
fragment_shader = """  
#version 330 core  
in vec4 vertexColor;  
out vec4 FragColor;  
void main()  
{  
    FragColor = vertexColor;  
}  
"""

# 编译着色器程序
shader_program = compileProgram(compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
                                compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER))

vertices = np.array([
    -0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0,
    0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0,
    0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
    -0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0, 1.0, 0.2, 0.5, 1.0,
], dtype=np.float32)

# 创建VBO
VBO = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_DYNAMIC_DRAW)

# 创建VAO
VAO = gl.glGenVertexArrays(1)
gl.glBindVertexArray(VAO)

# 设置顶点属性指针
stride = 8 * vertices.itemsize
gl.glVertexAttribPointer(0, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, None)
gl.glVertexAttribPointer(1, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(4 * vertices.itemsize))
gl.glEnableVertexAttribArray(0)
gl.glEnableVertexAttribArray(1)

# 解绑VAO和VBO
gl.glBindVertexArray(0)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)


def update_vertices():
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    new_colors = np.random.uniform(0, 1, (5, 3))
    for i in range(5):
        vertices[i * 8 + 4:i * 8 + 7] = new_colors[i]
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)


# 渲染循环
while not glfw.window_should_close(window):
    # 渲染
    gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    # 动态改变 不生效
    update_vertices()

    gl.glUseProgram(shader_program)
    gl.glPointSize(16.0)
    gl.glBindVertexArray(VAO)
    gl.glDrawArrays(gl.GL_POINTS, 0, 5)

    glfw.swap_buffers(window)
    glfw.poll_events()

# 退出时删除资源
gl.glDeleteVertexArrays(1, [VAO])
gl.glDeleteBuffers(1, [VBO])
gl.glDeleteProgram(shader_program)
glfw.terminate()
