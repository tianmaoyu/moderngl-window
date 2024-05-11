import glfw
from OpenGL.GL import *

import imgui
from imgui.integrations.glfw import GlfwRenderer


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
    background_color = (0.8, 0.8, 0.8, 1.0)
    imgui.create_context()
    #imgui 跟 window 绑定
    impl = GlfwRenderer(window, False)

    # 设置显示中文，字体为黑体
    io = imgui.get_io()
    fonts = io.fonts
    cn_font = io.fonts.add_font_from_file_ttf("C:/Windows/Fonts/hpsimplifiedhans-regular.ttf",16, None, fonts.get_glyph_ranges_chinese_full())
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        glClearNamedFramebufferfv(0, GL_COLOR, 0, background_color)

        impl.process_inputs()
        imgui.new_frame()
        imgui.push_font(cn_font)
        imgui.set_next_window_position(0, 0, condition=imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(300, 180, condition=imgui.FIRST_USE_EVER)
        imgui.begin("设置背景颜色")
        imgui.text("这是一个可以交互的演示程序：")
        _, color = imgui.color_edit3("颜色", background_color[0],background_color[1], background_color[2])
        background_color=(color[0], color[1], color[2], 1.0)
        imgui.end()
        imgui.pop_font()
        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)
        glfw.poll_events()

    impl.shutdown()
    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    run()
