#!/usr/bin/env python3
import sqlite3
import sys


def add_rule(domain, param):
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tracking_rules (domain, param) VALUES (?, ?)", (domain, param)
    )
    conn.commit()
    conn.close()
    print(f"Rule added: Domain='{domain}', Parameter='{param}'")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: add_rule.py <domain> <parameter>")
        sys.exit(1)

    arg_domain = sys.argv[1]
    arg_param = sys.argv[2]

    add_rule(arg_domain, arg_param)
