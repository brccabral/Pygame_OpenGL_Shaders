import pygame
import sys
import moderngl
import array

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
img = pygame.image.load("img.png")

# GPU version
# ctx = moderngl.create_context()

ctx = moderngl.create_standalone_context()
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

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(tex, uvs).rgb, 1.0);
}
"""

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# (2f 2f) => (vert texcoord)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])

while True:
    screen.fill((0, 0, 0))
    screen.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
