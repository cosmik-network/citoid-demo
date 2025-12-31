# Citation Metadata Fetcher

A Streamlit application that fetches and compares citation metadata from Wikipedia's Citoid API and your Zotero Translator Server deployment.

## Features

- 🔍 Fetch citation metadata for any URL or DOI
- 🔬 Compare results from Citoid API and Zotero Translator Server side-by-side
- 📋 Support for multiple citation formats (Zotero, BibTeX, MediaWiki)
- ⚡ Automatic endpoint detection (search for DOIs, web for URLs)
- 📥 Download citation data as JSON or BibTeX
- ✨ Clean and intuitive user interface

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

3. Set up credentials (for Zotero Translator Server comparison feature):

**Option A: Using Streamlit secrets (recommended for Streamlit Cloud)**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your credentials
```

**Option B: Using environment variables**
```bash
cp .env.example .env
# Edit .env and add your Zotero Translator Server credentials
```

Note: The app will work without credentials if you only use Citoid API (without comparison mode).

## Usage

Run the Streamlit app:
```bash
streamlit run citation_app.py
```

The app will open in your default browser at `http://localhost:8501`.

## How to Use

### Basic Mode (Citoid API only)

1. Enter a URL or DOI in the text input field
2. Select your preferred citation format from the dropdown
3. Click the "Fetch Citation" button
4. View the citation metadata
5. Optionally download the results

### Comparison Mode

1. Enable "Comparison Mode" checkbox
2. Enter a URL or DOI in the text input field
3. Click the "Fetch Citation" button
4. View side-by-side results from both APIs:
   - **Citoid API**: Wikipedia's citation service
   - **Zotero Translator Server**: Your AWS deployment
5. Compare the results and download from either source

## Supported Citation Formats

- **Zotero**: Comprehensive metadata format used by Zotero reference manager
- **MediaWiki**: Standard MediaWiki citation format
- **MediaWiki Base Fields**: Simplified MediaWiki format with essential fields
- **BibTeX**: LaTeX bibliography format

## Example Inputs to Try

### URLs (use `/web` endpoint)
- Academic papers: `https://arxiv.org/abs/2301.00001`
- News articles: `https://www.nature.com/articles/nature12373`
- Substack posts: `https://kevinmunger.substack.com/p/towards-the-post-naive-internet`
- GitHub repositories: `https://github.com/cosmik-network/semble`

### DOIs (use `/search` endpoint)
- `10.2307/4486062`
- `10.1038/nature12373`

## API Details

### Citoid API

This application uses the [Wikipedia Citoid API](https://www.mediawiki.org/wiki/Citoid):

```
https://en.wikipedia.org/api/rest_v1/data/citation/{format}/{url}
```

### Zotero Translator Server

The app also supports the [Zotero Translator Server](https://github.com/cosmik-network/zotero-translator-server) with two endpoints:

**Search endpoint** (for DOIs and other identifiers):
```bash
curl -H "x-api-key: YOUR-API-KEY" \
  -H "Content-Type: text/plain" \
  -d "10.2307/4486062" \
  "${API_URL}/search"
```

**Web endpoint** (for URLs):
```bash
curl -H "x-api-key: YOUR-API-KEY" \
  -H "Content-Type: text/plain" \
  -d "https://arxiv.org/abs/2301.00001" \
  "${API_URL}/web"
```

The app automatically detects whether to use `/search` or `/web` based on the input.

## Requirements

- Python 3.7+
- streamlit==1.29.0
- requests==2.31.0
- python-dotenv==1.0.0

## Configuration

### Local Development

You can configure credentials using either method:

**Option 1: Environment Variables (.env file)**
- `ZOTERO_API_URL`: Your Zotero Translator Server API endpoint
- `ZOTERO_API_KEY`: API key for authentication

**Option 2: Streamlit Secrets (.streamlit/secrets.toml)**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your credentials
```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy your app from the GitHub repository
4. In the app dashboard, go to **Settings > Secrets**
5. Add your secrets in TOML format:

```toml
[zotero]
api_url = "https://your-api-gateway-url.execute-api.region.amazonaws.com/prod"
api_key = "your-api-key-here"
```

6. Save and your app will automatically restart with the new secrets

For more information, see [Streamlit Secrets Management Documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).
