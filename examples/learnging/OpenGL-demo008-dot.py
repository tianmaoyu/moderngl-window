import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# 初始化GLFW
glfw.init()
window = glfw.create_window(800, 600, "OpenGL VAO VBO Example", None, None)
glfw.make_context_current(window)

# 编译着色器
vertex_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragment_src = """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

# 顶点数据
vertices = np.array([
    0.5, 0.5, 0.0,  # 右上角
    0.5, -0.5, 0.0,  # 右下角
    -0.5, -0.5, 0.0,  # 左下角
    -0.5, 0.5, 0.0, # 左上角
    -0.3, -0.5, 0.0,  # 左下角
], dtype=np.float32)

# 创建VAO和VBO
VAO = glGenVertexArrays(1)
print(VAO)
glBindVertexArray(VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices,GL_DYNAMIC_DRAW)

# 配置顶点属性指针
stride = vertices.strides[0]
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, 0)
glEnableVertexAttribArray(0)

# 渲染循环
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(6.0)
    glUseProgram(shader)
    glBindVertexArray(VAO)
    glDrawArrays(GL_POINTS, 0, 5)  # 使用GL_TRIANGLE_FAN绘制一个扇形（这里实际上是填充一个矩形）
    glfw.swap_buffers(window)

# 清理
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glfw.terminate()