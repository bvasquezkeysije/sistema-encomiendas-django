import os
import sys
import time

import psycopg2


def main():
    config = {
        "dbname": os.getenv("DB_NAME", ""),
        "user": os.getenv("DB_USER", ""),
        "password": os.getenv("DB_PASSWORD", ""),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
    }

    last_error = None
    for attempt in range(1, 31):
        try:
            connection = psycopg2.connect(**config)
            connection.close()
            print("Database connection ready.")
            return 0
        except psycopg2.OperationalError as exc:
            last_error = exc
            print(f"Waiting for database... attempt {attempt}/30")
            time.sleep(2)

    print(f"Database connection failed: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
