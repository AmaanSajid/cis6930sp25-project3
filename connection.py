#!/usr/bin/env python3
"""
check_connection.py  –  Quick health probe for a RabbitMQ broker.

Usage examples
--------------
# simplest: guest/guest on localhost:5672
python check_connection.py

# custom host, port, creds
python check_connection.py --host cpu002.cm.cluster --port 5672 \
                           --user student --password s3cret
"""
from __future__ import annotations
import argparse, sys, pika, ssl


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost",
                   help="RabbitMQ host (default localhost)")
    p.add_argument("--port", type=int, default=5672,
                   help="RabbitMQ port (default 5672)")
    p.add_argument("--user", default="guest",
                   help="Username (default guest)")
    p.add_argument("--password", default="guest",
                   help="Password (default guest)")
    p.add_argument("--vhost", default="/",
                   help="Virtual host (default /)")
    p.add_argument("--ssl", action="store_true",
                   help="Use TLS (AMQPS) on port 5671")
    args = p.parse_args()

    cred = pika.PlainCredentials(args.user, args.password)
    kw = dict(host=args.host,
              port=args.port,
              virtual_host=args.vhost,
              credentials=cred,
              blocked_connection_timeout=5,
              heartbeat=30)

    if args.ssl:
        context = ssl.create_default_context()
        kw["ssl_options"] = pika.SSLOptions(context)

    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(**kw))
        conn.close()
        print(f"✅  Connection OK — {args.host}:{args.port} login '{args.user}'")
        sys.exit(0)
    except Exception as e:        # pylint: disable=broad-except
        print(f"🚫  Connection FAILED — {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
