import os
import platform
import random
import sys
import time

from celery import Celery

app = Celery(broker="amqp://guest:guest@rabbitmq:5672//")


@app.task
def add(x, y):
    return x + y


def my_monitor(app):
    state = app.events.State()

    def announce_succeeded_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event["uuid"])

        print(
            "[Monitor %s@%s] TASK SUCCEEDED: %s[%s]"
            % (os.getpid(), platform.node(), task.name, task.uuid)
        )

        # Uncomment to simulate random monitor failure
        # if random.random() < 0.1:
        #     raise Exception("Random monitor failure occurred")

    with app.connection() as connection:
        recv = app.events.Receiver(
            connection,
            handlers={
                "task-succeeded": announce_succeeded_tasks,
                "*": state.event,
            },
            node_id="app_event_receiver",
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == "__main__":
    subcommand = sys.argv[-1]
    if subcommand == "producer":
        while True:
            time.sleep(1)
            add.delay(random.random(), random.random())
    elif subcommand == "consumer":
        app.worker_main(["worker", "--task-events"])
    elif subcommand == "monitor":
        my_monitor(app)
    else:
        print("Unknown subcommand. Usage: app.py {producer|monitor}")
