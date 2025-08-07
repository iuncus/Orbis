import numpy as np
# G = 6.67430e-11
G = 100
timestep = 1.0/120

distance_limit = 2000

class simulation:
    def __init__(self, bodies):
        self.bodies = bodies

    def step(self):
        net_forces = self.calc_forces()
        for i, body in enumerate(self.bodies):
            body.move(net_forces[i])
        # pass

    def calc_forces(self):

        net_forces = [np.zeros(2, dtype=float) for _ in self.bodies]

        for i, body1 in enumerate(self.bodies):
            for j in range(i + 1, len(self.bodies)):
                body2 = self.bodies[j]

            # for j, body2 in enumerate(self.bodies):
                # if  i == j: # same body
                #     continue



                r_vec = body2.position - body1.position
                distance = np.linalg.norm(r_vec)
                if distance == 0: # collision
                    continue
                # elif distance > distance_limit:
                    
                force_mag = G * body1.mass * body2.mass / distance  ** 2
                force_vec = force_mag * (r_vec/distance) # magnitude * unit vector

                net_forces[i] += force_vec
                net_forces[j] -= force_vec
    
        return net_forces



class body:
    def __init__(self, mass, velocity, position):
        # self.type = type
        self.mass = mass
        if mass >= 1000:
            self.type = "star"
        elif mass >= 10:
            self.type = "planet"
        else:
            self.type = "minor"
        self.velocity = np.array(velocity, dtype=float)
        self.position = np.array(position, dtype=float)

    def move(self, force):

        d_vec = force / self.mass * timestep
        self.position += self.velocity * timestep
        self.velocity += d_vec




def test():
    planet1 = body(1, (0., 0.), (0., 0.))
    planet2 = body(3e-6, (0., 6570.), (1., 0.))
    planet3 = body(66, (0.,0.), (1.00257, 0.))
    # sim = physics(planet1, planet2)
    sim = simulation((planet1, planet2, planet3))
    p1_pos = []
    p2_pos = []
    p3_pos = []
    for i in range(100000):
        sim.step()
        # planet1.position
    # print(sim.distance(planet1.position, planet2.position))
        p1_pos.append(planet1.position.copy())
        p2_pos.append(planet2.position.copy())
        p3_pos.append(planet3.position.copy())

        # print(planet1.position, planet2.position)

    print(len(p1_pos))
    # print(sim.gravity(planet1, planet2))
    import matplotlib.pyplot as plt
    p1_pos = np.array(p1_pos)
    p2_pos = np.array(p2_pos)
    p3_pos = np.array(p3_pos)

    plt.plot(p1_pos[:, 0], p1_pos[:, 1], 'r-', alpha=0.7, linewidth=1)
    plt.plot(p2_pos[:, 0], p2_pos[:, 1], 'b-', alpha=0.5, linewidth=1)
    plt.plot(p3_pos[:, 0], p3_pos[:, 1], 'g-', alpha=0.5, linewidth=1)


    plt.scatter(planet1.position[0], planet1.position[1], c='red', s=100, label='Planet 1 final')
    plt.scatter(planet2.position[0], planet2.position[1], c='blue', s=20, label='Planet 2 final')
    plt.scatter(planet3.position[0], planet3.position[1], c='green', s=20, label='Planet 3 final')

    plt.show()

# test()
