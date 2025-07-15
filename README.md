# Async Website Ping Tool

A Python CLI tool to asynchronously ping one or more websites and report the average response time for each.

## Features

- Asynchronously ping one or multiple URLs.
- Specify the number of pings per URL.
- Verbose mode for detailed output.
- Handles HTTP errors gracefully.
- Displays average response time or failure message per URL.

## Requirements

- Python 3.11+
- [httpx](https://www.python-httpx.org/)

Install dependencies:

```sh
pip install httpx
```

## Usage

```sh
python ping.py [-h] [-v] [-c COUNT] url
```

### Arguments

- `url`  
  URL(s) to ping. Separate multiple URLs with a comma (e.g., `google.com,github.com`).

### Options

- `-v`, `--verbose`  
  Enable verbose output.
- `-c COUNT`, `--count COUNT`  
  Number of pings per URL (default: 3).

### Example

```sh
python ping.py google.com,github.com -c 5 -v
```

## Output

- Shows average response time for each URL.
- If all requests fail for a URL, displays an error message.

---

**Author:** SOLO7899
