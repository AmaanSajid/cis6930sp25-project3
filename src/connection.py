#!/usr/bin/env python3
"""
Usage:
  python3 check_connection.py \
          --host cpu002.cm.cluster --port 5672 \
          --user STUDENT --password S3cret
"""
from __future__ import annotations
import argparse, sys, pika

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=5672)
    p.add_argument("--user", default="guest")
    p.add_argument("--password", default="guest")
    args = p.parse_args()

    params = pika.ConnectionParameters(
        host=args.host,
        port=args.port,
        credentials=pika.PlainCredentials(args.user, args.password),
        blocked_connection_timeout=5,
        heartbeat=30,
    )
    try:
        pika.BlockingConnection(params).close()
        print(f"✅  AMQP login OK → amqp://{args.user}@{args.host}:{args.port}")
        sys.exit(0)
    except Exception as e:                       # noqa: BLE001
        print(f"🚫  AMQP login FAILED: {e.__class__.__name__} – {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
