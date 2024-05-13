import numpy as np
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw

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
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

# 定义片段着色器
fragment_shader = """
#version 330
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f); // 设置颜色为橙色
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

# 创建VBO，返回id
VBO = gl.glGenBuffers(1)
#绑定
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
#复制到缓冲区 - vertices.nbytes：字节总数，vertices：数组
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

# 创建VAO,返回id
VAO = gl.glGenVertexArrays(1)
#绑定定点数组
gl.glBindVertexArray(VAO)
# 设置顶点属性指针
#location=0 每3个一组，float,是否归一化，步长-每个数据的多少字节，偏移量-从那里开始读取
gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * np.dtype(np.float32).itemsize, None)
#启用第一个数组
gl.glEnableVertexAttribArray(0)

# 解绑VAO和VBO
gl.glBindVertexArray(0)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

# 渲染循环
while not glfw.window_should_close(window):
    gl.glClearColor(0.2, 0.3, 0.3, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # 使用着色器程序
    gl.glUseProgram(shader_program)

    # 绘制线段
    gl.glBindVertexArray(VAO)
    gl.glDrawArrays(gl.GL_LINES, 0, 4)  # 两个线段，共四个顶点

    # 交换缓冲区并检查事件
    glfw.swap_buffers(window)
    glfw.poll_events()

# 退出时删除资源
gl.glDeleteVertexArrays(1, [VAO])
gl.glDeleteBuffers(1, [VBO])
gl.glDeleteProgram(shader_program)
glfw.terminate()
