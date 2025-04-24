# Why fork?

I forked this because I ran main through chatgpt and wanted to make a few changes. Wasn't ready to add them to upstream without validating them with a bit of usage.

# TracklessURL

**TracklessURL** is a Python-based tool that automatically cleans URLs copied to the clipboard by removing tracking parameters. It leverages a local SQLite database to manage tracking rules.

## Features

- Monitors clipboard for copied URLs.
- Automatically cleans URLs by removing tracking tokens such as `utm_source`, `utm_medium`, etc.
- Supports global tracking rules (for example, to match `utm_*` parameters across any domain).
- Manage custom rules for specific domains via a local SQLite database.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Confiqure/TracklessURL.git
cd TracklessURL
```

### 2. Set Up a Virtual Environment

To keep dependencies isolated, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Once everything is set up, you can start the clipboard monitor:

```bash
python main.py
```

## How It Works

1. **Clipboard Monitoring**:
   - The program continuously monitors your clipboard for copied URLs.
   - If a URL is detected, it is cleaned by removing unwanted tracking tokens.

2. **Rule Management**:
   - Rules for specific domains and global parameters (like `utm_*`) are stored in a SQLite database (`tracking_params.db`).
   - You can add, view, or delete rules to customize the cleaning process.

## Usage

### Adding Rules

You can easily add new rules to remove parameters from URLs using the script. For example:

```python
add_rule('*', 'utm_source')  # Global rule for utm_source
add_rule('open.spotify.com', 'si')  # Rule for a specific domain
```

### Viewing Rules

To view existing rules, simply call the function:

```python
view_rules()
```

### Deleting Rules

To delete a rule by its ID:

```python
delete_rule(rule_id)
```

## Managing Rules via Command Line

TracklessURL provides two command-line scripts to easily manage tracking rules:

- **add_rule.py**: Adds a new rule to the SQLite database.
- **remove_rule.py**: Removes an existing rule by its ID.

### 1. Setting Up

To make the scripts executable, run the following commands:

   ```bash
   chmod +x add_rule.py
   chmod +x remove_rule.py
   ```

### 2. Adding a New Rule

You can add a rule by specifying the domain and the parameter you want to remove. Use the `add_rule.py` script as follows:

```bash
./add_rule.py <domain> <parameter>
```

#### New Rule Example

```bash
./add_rule.py "open.spotify.com" "si"
```

This will add a rule to remove the `si` parameter from URLs under the domain `open.spotify.com`.

### 3. Removing a Rule by ID

You can remove a rule by its ID using the `remove_rule.py` script. First, view the existing rules using the `view_rules()` function, then use the ID of the rule you want to remove:

```bash
./remove_rule.py <rule_id>
```

#### Remove Rule Example

```bash
./remove_rule.py 1
```

This will remove the rule with ID `1`.

### 4. Adding Scripts to Path (Optional)

If you'd like to run these commands from anywhere in your terminal, you can add the project directory to your `$PATH`. Add the following line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PATH="$PATH:/path/to/TracklessURL"
```

After updating your shell configuration, run `source ~/.bashrc` (or `source ~/.zshrc`) to apply the changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
