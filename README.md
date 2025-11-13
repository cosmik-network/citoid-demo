# Citation Metadata Fetcher

A simple Streamlit application that fetches citation metadata using Wikipedia's Citoid API.

## Features

- 🔍 Fetch citation metadata for any URL
- 📋 Support for multiple citation formats (Zotero, BibTeX, MediaWiki)
- 📥 Download citation data as JSON
- ✨ Clean and intuitive user interface
- ⚡ Real-time API request tracking
- 🛡️ Robust error handling

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd citoid-demo
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run citation_app.py
```

The app will open in your default browser at `http://localhost:8501`.

## How to Use

1. Enter a URL in the text input field
2. Select your preferred citation format from the dropdown
3. Click the "Fetch Citation" button
4. View the citation metadata in JSON format
5. Optionally download the results as a JSON file

## Supported Citation Formats

- **Zotero**: Comprehensive metadata format used by Zotero reference manager
- **MediaWiki**: Standard MediaWiki citation format
- **MediaWiki Base Fields**: Simplified MediaWiki format with essential fields
- **BibTeX**: LaTeX bibliography format

## Example URLs to Try

- Academic papers: `https://arxiv.org/abs/1706.03762`
- News articles: `https://www.bbc.com/news`
- Wikipedia articles: `https://en.wikipedia.org/wiki/Artificial_intelligence`
- GitHub repositories: `https://github.com/streamlit/streamlit`

## API Details

This application uses the [Wikipedia Citoid API](https://www.mediawiki.org/wiki/Citoid):

```
https://en.wikipedia.org/api/rest_v1/data/citation/{format}/{url}
```

## Requirements

- Python 3.7+
- streamlit==1.29.0
- requests==2.31.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
