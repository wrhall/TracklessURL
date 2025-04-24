import sqlite3
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import pyperclip

# Optional logging toggle
LOGGING_ENABLED = True

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            param TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Add a new tracking rule with validation
def add_rule(domain, param):
    if not domain or not param:
        raise ValueError("Domain and parameter must not be empty")
    if any(c in domain for c in " ;'\"") or any(c in param for c in " ;'\""):
        raise ValueError("Invalid characters in domain or parameter")

    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tracking_rules (domain, param) VALUES (?, ?)", (domain, param)
    )
    conn.commit()
    conn.close()


# View all tracking rules
def view_rules():
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracking_rules ORDER BY domain, param")
    rules = cursor.fetchall()
    conn.close()
    return rules


# Delete a rule by ID
def delete_rule(rule_id):
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tracking_rules WHERE id=?", (rule_id,))
    conn.commit()
    conn.close()


# Get tracking parameters for a specific domain or wildcard
def get_tracking_params(domain):
    conn = sqlite3.connect("tracking_params.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT param FROM tracking_rules WHERE domain=? OR domain='*'", (domain,)
    )
    params = [row[0] for row in cursor.fetchall()]
    conn.close()
    return params


# Normalize domain (remove www., lowercase)
def normalize_domain(domain):
    return domain.lower().lstrip("www.")


# Clean the URL by removing tracking parameters
def clean_url(url):
    parsed_url = urlparse(url)
    domain = normalize_domain(parsed_url.netloc)

    tracking_params = get_tracking_params(domain)

    if "ALL" in [p.upper() for p in tracking_params]:
        cleaned_url = urlunparse(parsed_url._replace(query=""))
        return cleaned_url

    if tracking_params:
        query_params = parse_qs(parsed_url.query)
        clean_params = {
            k: v for k, v in query_params.items() if k not in tracking_params
        }
        new_query = urlencode(clean_params, doseq=True)
        cleaned_url = urlunparse(parsed_url._replace(query=new_query))

        if cleaned_url != url and LOGGING_ENABLED:
            print(f"[Cleaned] {url} -> {cleaned_url}")
        elif LOGGING_ENABLED:
            print(f"[Unchanged] {url}")

        return cleaned_url

    return url


# Main loop to monitor clipboard and clean URLs
def main():
    last_clipboard = ""
    last_cleaned_content = ""

    print("Monitoring clipboard for URLs... Press Ctrl+C to exit.")
    try:
        while True:
            try:
                clipboard_content = pyperclip.paste()
            except Exception as e:
                print(f"[Error accessing clipboard] {e}")
                time.sleep(1)
                continue

            if clipboard_content != last_clipboard and clipboard_content != last_cleaned_content:
                lines = clipboard_content.splitlines()
                cleaned_lines = []

                for line in lines:
                    original_line = line
                    line = line.strip()
                    if line.startswith(("http://", "https://")):
                        cleaned_line = clean_url(line)
                        cleaned_lines.append(cleaned_line)
                    else:
                        cleaned_lines.append(original_line)

                final_content = "\n".join(cleaned_lines)
                if final_content != clipboard_content:
                    last_cleaned_content = final_content
                    pyperclip.copy(final_content)

            last_clipboard = clipboard_content
            time.sleep(1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    init_db()
    print("Current tracking rules:")
    for rule in view_rules():
        print(rule)

    main()
