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
launch_multiplier = 3
exit = False

clock = pygame.time.Clock()
FIXED_TIMESTEP = 1.0/120
accumulator = 0.

sun = body(100000, (0, 0), (width//2, height//2))
bodies_list = [sun]
sim = simulation(bodies_list)
mouse_down = False
ghost_bodies = []
while not exit:

    dt = clock.tick(60) / 1000.0 # get dt in seconds
    accumulator += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            click_coord = pygame.mouse.get_pos()


            
        elif event.type == pygame.MOUSEBUTTONUP:
            release_coord = pygame.mouse.get_pos()
            # velocity = ((release_coord[0] - click_coord[0]) //10 , (release_coord[1] - click_coord[1]) //10 ) 
            velocity = ((click_coord[0] - release_coord[0]) * launch_multiplier, (click_coord[1] - release_coord[1]) * launch_multiplier) 
            

            planet = body(10, velocity, click_coord)
            # pygame.draw.circle(canvas, red, planet.position, (100 - 800000 // planet.mass))
            pygame.draw.circle(canvas, blue, planet.position, 5)
            

            bodies_list.append(planet)
            # sim = simulation(bodies_list)
            mouse_down = False

    canvas.fill((0,0,0))

    # drop new planet
    if mouse_down and click_coord:
        pygame.draw.circle(canvas, blue, click_coord, 5)
        mouse_pos = pygame.mouse.get_pos()
        # ghost_bodies = bodies_list.copy()
        ghost_bodies = [body(b.mass, b.velocity, b.position) for b in bodies_list if b.mass >= 1000]
        # print(ghost_bodies)

        velocity = ((click_coord[0] - mouse_pos[0]) * launch_multiplier, (click_coord[1] - mouse_pos[1]) * launch_multiplier)
        ghost = body(10, velocity, click_coord)
        ghost_bodies.append(ghost)
        ghost_sim = simulation(ghost_bodies)

        # draw expected trajectory 
        if click_coord != mouse_pos:
            trajectory = []
            for i in range(70):
                pos = ghost.position.copy()
                ghost_sim.step()
                # new_pos = ghost_body.position
                trajectory.append(pos)

            pygame.draw.aalines(canvas, blue, False, trajectory, 1)
            # print(trajectory)
                # pygame.draw.line(canvas, blue, click_coord, ((click_coord[0] * 2 - mouse_pos[0]), ((click_coord[1] * 2 - mouse_pos[1]))))



    while accumulator >= FIXED_TIMESTEP:

        sim.step()  
        accumulator -= FIXED_TIMESTEP


    for i in bodies_list:
        if i.mass >= 2000:
            colour = red
            size = 15
        else:
            colour = blue 
            size = 5
        # print(i.position)
        # pygame.draw.circle(canvas, colour, i.position, size)
        gfxdraw.aacircle(canvas, int(i.position[0]), int(i.position[1]), size, colour)
        gfxdraw.filled_circle(canvas, int(i.position[0]), int(i.position[1]), size, colour)

    # print(clock.get_fps())

    pygame.display.update()
    # clock.tick(60)