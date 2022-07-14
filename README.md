# High-availability Celery monitor

An example Celery application which runs multiple instances of a real-time
Celery events consumer. This technique can be used to improve the availability
of an events consumer in production by enabling multiple consumers to be
deployed at once.

The technique shown here is discussed in more detail in [my blog post][blog].
All credit goes to [@isNeil][neil] for discovering the `node_id` solution!

## Running

Start the task producer, task consumer, event monitor, and message broker using
the Docker Compose file provided.

```
$ docker compose up --scale=monitor=N
```

Replace `N` with the number of monitor instances to run. Setting this to a
value greater than one will result in even distribution of events across the
monitors. For example when `N` is replaced with `2` the logs like this:

```
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[2eba467f-e786-4010-86e2-8bb0bdb6fe8f]
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[f0652fb4-298f-4863-a18e-9632261b2135]
high-availability-celery-monitor-monitor-1   | [Monitor 1@63c97c300c52] TASK SUCCEEDED: None[aa4e4a9f-7cfe-42f6-9169-e8abe4e698c7]
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[8b868528-9375-481a-9ab8-0b6a1010d90a]
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[b7ce7cea-ea6a-4aaa-843a-3c6b31a74959]
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[0cb8ebb3-3969-4ddd-9999-8f98a7cc4267]
high-availability-celery-monitor-monitor-2   | [Monitor 1@95a02df38f29] TASK SUCCEEDED: __main__.add[39abe46e-1244-44de-8d26-77a66ddcb407]
high-availability-celery-monitor-monitor-1   | [Monitor 1@63c97c300c52] TASK SUCCEEDED: __main__.add[e1c0f0b8-9835-4ebb-bfcf-229fac936ef7]
```

(The two monitor hostnames here are `63c97c300c52` and `95a02df38f29`.)

Note the `None` task name is due to the example monitor using [Celery's
in-memory `app.events.State` task store][celery-state-store], which aggregates
task information across all events belonging to a given task. As a single
monitor may not receive all events for a given task this store may not contain
all information on a task even after it has completed.

[celery-events]: https://docs.celeryq.dev/en/stable/userguide/monitoring.html#real-time-processing
[celery-state-store]: https://docs.celeryq.dev/en/stable/reference/celery.events.state.html
[blog]: https://alexpearce.me/2022/07/high-availability-celery-monitoring/
[neil]: https://github.com/isNeil
