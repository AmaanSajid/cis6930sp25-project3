"""
Project-3 command-line tool.

Usage examples
--------------
# consume queue
python -m src.main --consume --command localhost --port 5672

# build reports
python -m src.main --report
"""
from __future__ import annotations
import argparse
from loguru import logger


def _parse_args():
    p = argparse.ArgumentParser("proj-3")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--consume", action="store_true",
                      help="Start RabbitMQ consumer")
    mode.add_argument("--report", action="store_true",
                      help="Generate PDF reports")
    p.add_argument("--command", help="RabbitMQ host")
    p.add_argument("--port", type=int, default=5672)
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    if args.consume:
        # inject host/port and start consumer
        from src.consumer import RABBIT, consume_forever
        if not args.command:
            raise SystemExit("--command (host) is required in consume mode")
        RABBIT.update(host=args.command, port=args.port)
        consume_forever()
    else:
        # build reports
        from src.visualize import make_reports
        logger.info("🖨️  Generating PDF reports…")
        make_reports()


if __name__ == "__main__":
    main()
