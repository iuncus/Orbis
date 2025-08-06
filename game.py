import pygame
from pygame import gfxdraw
from physics import simulation, body
pygame.init()

height = 1200
width = 1200
red = (255, 0, 0)
blue = (0, 0, 255)
canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Orbis")

exit = False


sun = body(10000, (0, 0), (width//2, height//2))
bodies_list = [sun]
sim = simulation(bodies_list)
mouse_down = False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            click_coord = pygame.mouse.get_pos()


            
        elif event.type == pygame.MOUSEBUTTONUP:
            release_coord = pygame.mouse.get_pos()
            # velocity = ((release_coord[0] - click_coord[0]) //10 , (release_coord[1] - click_coord[1]) //10 ) 
            velocity = ((click_coord[0] - release_coord[0]) //5 , (click_coord[1] - release_coord[1]) //10 ) 
            

            planet = body(10, velocity, click_coord)
            # pygame.draw.circle(canvas, red, planet.position, (100 - 800000 // planet.mass))
            pygame.draw.circle(canvas, blue, planet.position, 5)
            

            bodies_list.append(planet)
            # sim = simulation(bodies_list)
            mouse_down = False

    canvas.fill((0,0,0))
    if mouse_down and click_coord:
        pygame.draw.circle(canvas, blue, click_coord, 5)
        mouse_pos = pygame.mouse.get_pos()
        if click_coord != mouse_pos:
            pygame.draw.line(canvas, blue, click_coord, ((click_coord[0] * 2 - mouse_pos[0]), ((click_coord[1] * 2 - mouse_pos[1]))))



    sim.step()  

    for i in bodies_list:
        if i.mass >= 2000:
            colour = red
            size = 15
        else:
            colour = blue 
            size = 5

        pygame.draw.circle(canvas, colour, i.position, size)


    pygame.display.update()
