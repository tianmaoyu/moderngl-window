import numpy as np
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import time

# 初始化glfw库
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# 创建一个窗口
window = glfw.create_window(800, 600, "VAO and VBO Example", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# 设置上下文
glfw.make_context_current(window)

# 定义顶点着色器
vertex_shader = """
#version 330
layout (location = 0) in vec3 aPos;
uniform vec3 offset; // 用于偏移的uniform变量
void main()
{
    gl_Position = vec4(aPos + offset, 1.0);
}
"""

# 定义片段着色器
fragment_shader = """
#version 330
out vec4 FragColor;
uniform vec3 color; // 用于颜色的uniform变量
void main()
{
    FragColor = vec4(color, 1.0); // 使用uniform变量设置颜色
}
"""

# 编译着色器程序
shader_program = compileProgram(compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
                                compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER))

# 顶点数据，表示两条线段
vertices = np.array([
    -0.5, -0.5, 0.0,  # 第一个线段的第一个顶点
    0.5, -0.5, 0.0,  # 第一个线段的第二个顶点
    -0.5, 0.5, 0.0,  # 第二个线段的第一个顶点
    0.5, 0.5, 0.0  # 第二个线段的第二个顶点
], dtype=np.float32)

# 创建VBO
VBO = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_DYNAMIC_DRAW)

# 创建VAO
VAO = gl.glGenVertexArrays(1)
gl.glBindVertexArray(VAO)

# 设置顶点属性指针
gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * np.dtype(np.float32).itemsize, None)
gl.glEnableVertexAttribArray(0)

# 解绑VAO和VBO
gl.glBindVertexArray(0)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

# 获取uniform位置
offset_location = gl.glGetUniformLocation(shader_program, "offset")
color_location = gl.glGetUniformLocation(shader_program, "color")

# 渲染循环
start_time = time.time()
while not glfw.window_should_close(window):
    current_time = time.time() - start_time

    # 更新顶点数据
    offset = np.array([np.sin(current_time) * 0.5, np.cos(current_time) * 0.5, 0.0], dtype=np.float32)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, offset.nbytes, offset)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    # 更新颜色
    color = 0.5 * np.array([np.sin(current_time), np.cos(current_time), 0.0], dtype=np.float32) + 0.5

    # 渲染
    gl.glClearColor(0.2, 0.3, 0.3, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glUseProgram(shader_program)

    # 传递uniform变量
    gl.glUniform3fv(offset_location, 1, offset)
    gl.glUniform3fv(color_location, 1, color)

    gl.glBindVertexArray(VAO)
    gl.glDrawArrays(gl.GL_LINES, 0, 4)

    glfw.swap_buffers(window)
    glfw.poll_events()

# 退出时删除资源
gl.glDeleteVertexArrays(1, [VAO])
gl.glDeleteBuffers(1, [VBO])
gl.glDeleteProgram(shader_program)
glfw.terminate()
