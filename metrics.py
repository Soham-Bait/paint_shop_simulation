class Metrics:

    def __init__(self):

        # throughput
        self.total_completed = 0

        # system time
        self.system_times = []

        # waiting times
        self.clean_wait = []
        self.primer_wait = []
        self.paint_wait = []

        # queue tracking
        self.max_clean_queue = 0
        self.max_primer_queue = 0
        self.max_paint_queue = 0

        # machine busy times
        self.clean_busy = 0
        self.primer_busy = 0
        self.paint_busy = 0

        # alert counter
        self.alerts = 0