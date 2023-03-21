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

while True:
    screen.fill((0, 0, 0))
    screen.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
