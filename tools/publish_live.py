"""
publish_live.py – continuously publish UFO-sighting messages
to the *fan-out* exchange ``ufo`` on the local RabbitMQ broker.

Adds a 30 % chance that the `msg` field is “alien” gibberish so that
your classifier labels roughly one-third of the stream as alien.
"""
from __future__ import annotations
import json, random, time
from faker import Faker
import pika

# --------------------------------------------------------------------------
# Connection (guest/guest on localhost; works inside and outside Docker)
# --------------------------------------------------------------------------
PARAMS = pika.ConnectionParameters(
    host="rabbit",   # container name resolves to localhost when run outside
    port=5672,
    credentials=pika.PlainCredentials("guest", "guest"),
)

# --------------------------------------------------------------------------
# Message factories
# --------------------------------------------------------------------------
fake   = Faker()
shapes = ["circle", "triangle", "disk", "cigar", "sphere", "oval"]

def make_human() -> str:
    """English-like sentence (classifier → human)."""
    return fake.sentence(nb_words=random.randint(6, 10)).rstrip(".")

ALIEN_SYLLABLES = ["zog", "blar", "quix", "phl", "narg", "vrr"]

def make_alien() -> str:
    """Gibberish string (classifier → alien)."""
    return " ".join(random.choice(ALIEN_SYLLABLES)
                    for _ in range(random.randint(5, 9)))

# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------
conn = pika.BlockingConnection(PARAMS)
ch   = conn.channel()
ch.exchange_declare(exchange="ufo", exchange_type="fanout")

print("🚀  Live publisher running — 1 msg/sec (≈30 % alien)")
while True:
    is_alien = random.random() < 0.30           # 30 % gibberish
    msg_body = make_alien() if is_alien else make_human()

    payload = {
        "ts": time.time(),
        "lat": random.uniform(-90, 90),
        "lon": random.uniform(-180, 180),
        "shape": random.choice(shapes),
        "msg": msg_body,
    }
    ch.basic_publish(exchange="ufo", routing_key="", body=json.dumps(payload))
    time.sleep(1)
