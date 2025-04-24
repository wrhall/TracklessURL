import sqlite3

conn = sqlite3.connect("tracking_params.db")
cursor = conn.cursor()

# Replace any param='*' with param='ALL'
cursor.execute("""
    UPDATE tracking_rules
    SET param='ALL'
    WHERE param='*'
""")

conn.commit()
conn.close()

print("All rules with param='*' updated to param='ALL'.")
