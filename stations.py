import simpy
import config


class PaintShopStations:

    def __init__(self, env):

        # Cleaning station (1 machine)
        self.cleaning = simpy.Resource(env, capacity=config.CLEAN_CAPACITY)

        # Primer station (2 machines working in parallel)
        self.primer = simpy.Resource(env, capacity=config.PRIMER_CAPACITY)

        # Painting station (1 machine)
        self.painting = simpy.Resource(env, capacity=config.PAINT_CAPACITY)