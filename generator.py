import random
import config
from car_process import car


def car_generator(env, stations, metrics):

    # Counter to assign IDs to incoming cars
    car_id = 0

    while True:

        # Generate time between car arrivals (8–12 minutes)
        interarrival = random.uniform(config.ARRIVAL_MIN, config.ARRIVAL_MAX)

        # Stop creating new cars if next arrival exceeds shift time
        if env.now + interarrival > config.SIMULATION_TIME:
            break

        # Wait until the next car arrives
        yield env.timeout(interarrival)

        car_id += 1

        # Start a new car process in the simulation
        env.process(car(env, car_id, stations, metrics))