import simpy
import config

from stations import PaintShopStations
from metrics import Metrics
from generator import car_generator


def run_simulation():

    env = simpy.Environment()

    stations = PaintShopStations(env)
    metrics = Metrics()

    env.process(car_generator(env, stations, metrics))

    # Run only for shift duration
    env.run(until=config.SIMULATION_TIME)

    print("\n=== Paint Shop Simulation Results (480 minutes) ===")

    avg_system = (
        sum(metrics.system_times) / len(metrics.system_times)
        if metrics.system_times
        else 0
    )

    clean_util = (metrics.clean_busy / config.SIMULATION_TIME) * 100
    primer_util = (metrics.primer_busy / (config.SIMULATION_TIME * config.PRIMER_CAPACITY)) * 100
    paint_util = (metrics.paint_busy / config.SIMULATION_TIME) * 100

    avg_clean_wait = (
        sum(metrics.clean_wait) / len(metrics.clean_wait)
        if metrics.clean_wait
        else 0
    )

    avg_primer_wait = (
        sum(metrics.primer_wait) / len(metrics.primer_wait)
        if metrics.primer_wait
        else 0
    )

    avg_paint_wait = (
        sum(metrics.paint_wait) / len(metrics.paint_wait)
        if metrics.paint_wait
        else 0
    )

    print(f"Total cars completed: {metrics.total_completed}")
    print(f"Average system time per car: {avg_system:.2f} minutes\n")

    print("Station 1 (Cleaning):")
    print(f"- Utilization: {clean_util:.2f}%")
    print(f"- Max queue: {metrics.max_clean_queue} cars")
    print(f"- Avg wait time: {avg_clean_wait:.2f} minutes\n")

    print("Station 2 (Primer):")
    print(f"- Utilization: {primer_util:.2f}%")
    print(f"- Max queue: {metrics.max_primer_queue} cars")
    print(f"- Avg wait time: {avg_primer_wait:.2f} minutes\n")

    print("Station 3 (Painting):")
    print(f"- Utilization: {paint_util:.2f}%")
    print(f"- Max queue: {metrics.max_paint_queue} cars")
    print(f"- Avg wait time: {avg_paint_wait:.2f} minutes\n")

    print(f"Alerts triggered: {metrics.alerts}")


if __name__ == "__main__":
    run_simulation()