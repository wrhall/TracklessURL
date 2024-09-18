#!/usr/bin/env python3
import sqlite3
import sys


def delete_rule(rule_id):
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tracking_rules WHERE id=?", (rule_id,))
    conn.commit()
    conn.close()
    print(f"Rule with ID={rule_id} removed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: remove_rule.py <rule_id>")
        sys.exit(1)

    arg_rule_id = sys.argv[1]

    delete_rule(arg_rule_id)
