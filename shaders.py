import pygame
import sys
import moderngl
import array

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((800, 600))
clock = pygame.time.Clock()
img = pygame.image.load("img.png")

ctx = moderngl.create_context()
print(ctx.version_code)
# position (x,y), uv coords (x, y)
# 1 |   /| 2
#   |  / |
#   | /  |
# 3 |/___| 4
# openGL is [-1 to 1]
# uv is [0 to 1]
quad_buffer = ctx.buffer(
    data=array.array(
        "f",
        [
            # top left (xp1, yp1), (xu1, yu1)
            -1.0,
            1.0,
            0.0,
            0.0,
            # top right (xp2, yp2), (xu2, yu2)
            1.0,
            1.0,
            1.0,
            0.0,
            # bottom left (xp3, yp3), (xu3, yu3)
            -1.0,
            -1.0,
            0.0,
            1.0,
            # bottom right (xp4, yp4), (xu4, yu4)
            1.0,
            -1.0,
            1.0,
            1.0,
        ],
    )
)

vert_shader = """
#version 330 core

in vec2 vert; // position
in vec2 texcoord; // uvs
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""

# uniform - passed to all parallel gpu
# in - passed by each call a different buffer value
frag_shader = """
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 10 + time * 0.01) * 0.1, uvs.y);
    f_color = vec4(texture(tex, sample_pos).rg, texture(tex, sample_pos).b * 1.5, 1.0);
}
"""

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# (2f 2f) => (vert texcoord)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])


def surf_to_texture(surf: pygame.Surface):
    """helper function to convert pygame surface into openGL texture"""
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (
        moderngl.NEAREST,
        moderngl.NEAREST,
    )  # scale up method (2x2 to 1000x1000)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view("1"))  # get raw data
    return tex


t = 0

while True:
    t += 1
    display.fill((0, 0, 0))
    display.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program["tex"] = 0
    program["time"] = t
    render_object.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()

    frame_tex.release()

    clock.tick(60)
