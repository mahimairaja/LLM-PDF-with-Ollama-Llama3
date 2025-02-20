# PDF Data Extraction

A Python tool to extract data along with tables from PDF files and convert them to JSON or Markdown format.

## Prerequisites

- Python 3.8+
- Ollama (for LLM support)

### Ollama Installation

```bash
$ curl -fsSL https://ollama.com/install.sh | sh
```

### Pull LLM Model

```bash
$ ollama pull llama3.1:8b

# You can check the list of available models using the following command:
$ ollama list
```

## Setup

1. Clone the repository
2. Install dependencies:
```bash
$ pip install -r requirements.txt
```
3. Ensure Ollama is running locally at http://127.0.0.1:11434/

## Usage

Run the script using the following command:

```bash
$ python main.py <pdf_file> --output-format <format> --output-dir <directory>
```

### Arguments

- `pdf_file`: Path to the input PDF file
- `--output-format`: Format of the output (json or markdown)
- `--output-dir`: Directory to save the output file (default: output)

### Examples

```bash
# Convert to JSON
$ python main.py data.pdf --output-format json --output-dir output

# Convert to Markdown
$ python main.py data.pdf --output-format markdown --output-dir output
```

## Features

- Supports PDF with table extraction
- Multiple output formats (JSON, Markdown)
- LLM integration using Ollama
- Automatic output directory creation
- Progress tracking and status messages

## Configuration

The tool uses the following default configuration:
- LLM: llama3.1:8b
- Ollama base URL: http://127.0.0.1:11434/