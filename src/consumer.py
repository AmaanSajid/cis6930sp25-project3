"""
Consume UFO‐sighting messages from a RabbitMQ *fanout* exchange called 'ufo',
classify each message, and append the result to output/messages.csv.
"""
from __future__ import annotations
import csv, json, pathlib
import pika
from loguru import logger
from .classifier import label
# Exchange is fixed by spec; host/port injected by main.py
RABBIT: dict[str, str | int] = {"exchange": "ufo", "exch_type": "fanout"}


OUTDIR = pathlib.Path("output")
OUTDIR.mkdir(exist_ok=True)
CSV_PATH = OUTDIR / "messages.csv"
LOG_PATH = OUTDIR / "run.log"
credentials = pika.PlainCredentials("guest", "guest")   # ← hard-coded defaults



logger.add(LOG_PATH, rotation="10 MB", serialize=True)


def consume_forever() -> None:
    params = pika.ConnectionParameters(RABBIT["host"], RABBIT["port"],
                                  credentials=credentials, heartbeat=60)
    with pika.BlockingConnection(params) as conn, conn.channel() as ch:
        ch.exchange_declare(exchange=RABBIT["exchange"],
                            exchange_type=RABBIT["exch_type"])
        q = ch.queue_declare(queue="", exclusive=True)
        ch.queue_bind(exchange=RABBIT["exchange"], queue=q.method.queue)

        with CSV_PATH.open("a", newline="") as fh:
            writer = csv.writer(fh)
            logger.info("📡  Listening on {}:{}", RABBIT["host"], RABBIT["port"])
            for method, props, body in ch.consume(q.method.queue,
                                                  inactivity_timeout=1):
                if body is None:       # heartbeat timeout
                    continue
                data = json.loads(body)          # ts, lat, lon, shape, msg
                data["label"] = label(data["msg"])
                writer.writerow(data.values())
                logger.info("classified {}", data)
                fh.flush()
