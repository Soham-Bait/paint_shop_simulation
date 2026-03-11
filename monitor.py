import config


def check_queue(env, queue_length, station_name, metrics):

    # Check if the queue exceeds the alert threshold
    if queue_length > config.QUEUE_ALERT:

        # Print warning message with station name and current time
        print(f"ALERT: Queue at {station_name} has {queue_length} cars waiting at time {env.now}")

        # Count how many alerts occurred during the simulation
        metrics.alerts += 1