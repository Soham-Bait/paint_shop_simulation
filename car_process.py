import random
import config
from monitor import check_queue


def car(env, car_id, stations, metrics):

    # Time when the car enters the system
    arrival_time = env.now

    print(f"[{env.now}] Car {car_id} arrives")

    # ---------- CLEANING ----------

    # Check current queue length and update max queue
    queue_len = len(stations.cleaning.queue)
    metrics.max_clean_queue = max(metrics.max_clean_queue, queue_len)

    # Trigger alert if queue gets too long
    check_queue(env, queue_len, "Cleaning", metrics)

    start_wait = env.now

    # Request cleaning machine (only 1 available)
    with stations.cleaning.request() as req:
        yield req

        # Record waiting time before service
        wait = env.now - start_wait
        metrics.clean_wait.append(wait)

        print(f"[{env.now}] Car {car_id} starts Cleaning")

        # Random cleaning time
        process_time = random.uniform(
            config.CLEAN_TIME_MIN, config.CLEAN_TIME_MAX
        )

        metrics.clean_busy += process_time

        yield env.timeout(process_time)

        print(f"[{env.now}] Car {car_id} finishes Cleaning")

    # ---------- PRIMER ----------

    queue_len = len(stations.primer.queue)
    metrics.max_primer_queue = max(metrics.max_primer_queue, queue_len)

    check_queue(env, queue_len, "Primer", metrics)

    start_wait = env.now

    # Primer station has 2 machines
    with stations.primer.request() as req:
        yield req

        wait = env.now - start_wait
        metrics.primer_wait.append(wait)

        print(f"[{env.now}] Car {car_id} starts Primer")

        process_time = random.uniform(
            config.PRIMER_TIME_MIN, config.PRIMER_TIME_MAX
        )

        metrics.primer_busy += process_time

        yield env.timeout(process_time)

        print(f"[{env.now}] Car {car_id} finishes Primer")

    # ---------- PAINTING ----------

    queue_len = len(stations.painting.queue)
    metrics.max_paint_queue = max(metrics.max_paint_queue, queue_len)

    check_queue(env, queue_len, "Painting", metrics)

    start_wait = env.now

    # Painting stage (1 machine)
    with stations.painting.request() as req:
        yield req

        wait = env.now - start_wait
        metrics.paint_wait.append(wait)

        print(f"[{env.now}] Car {car_id} starts Painting")

        process_time = random.uniform(
            config.PAINT_TIME_MIN, config.PAINT_TIME_MAX
        )

        metrics.paint_busy += process_time

        yield env.timeout(process_time)

        print(f"[{env.now}] Car {car_id} finishes Painting")

    # ---------- EXIT ----------

    # Total time spent in system
    total_time = env.now - arrival_time

    metrics.system_times.append(total_time)
    metrics.total_completed += 1

    print(f"[{env.now}] Car {car_id} exits system")