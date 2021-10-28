# Habr proxy

A simple http proxy server running locally that shows the contents of the Habr pages.
The proxy modifies the text on the pages as follows: adds "™" after each six-letter word.

## Requirements

- Python 3.8+

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd src
python main.py
```

## Tests

```bash
pytest
```