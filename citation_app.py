"""
Streamlit Citation Metadata Fetcher
Uses Wikipedia's Citoid API to fetch citation metadata for any URL
"""

import streamlit as st
import requests
from urllib.parse import quote
import json
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()


def fetch_citation(url, format_type="zotero"):
    """
    Fetch citation metadata from Citoid API

    Args:
        url: The URL to fetch citation data for
        format_type: Citation format (mediawiki, mediawiki-basefields, zotero, bibtex)

    Returns:
        dict: Response from the API or error details
    """
    try:
        # Encode the URL
        encoded_url = quote(url, safe="")

        # Build the API endpoint
        api_url = f"https://en.wikipedia.org/api/rest_v1/data/citation/{format_type}/{encoded_url}"

        # Set headers with User-Agent
        headers = {"User-Agent": "Streamlit-Citation-Fetcher/1.0 (Educational Project)"}

        # Make the API call
        response = requests.get(api_url, headers=headers, timeout=10)

        # Raise exception for bad status codes
        response.raise_for_status()

        # Parse response based on format type
        # BibTeX returns plain text, others return JSON
        if format_type == "bibtex":
            data = response.text
            is_json = False
        else:
            data = response.json()
            is_json = True

        return {
            "success": True,
            "data": data,
            "is_json": is_json,
            "format_type": format_type,
            "api_url": api_url,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection error. Please check your internet connection.",
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP error: {e.response.status_code} - {e.response.reason}",
        }
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}


def is_doi_or_identifier(text):
    """
    Check if the input is a DOI or other identifier (vs a full URL)

    Args:
        text: The input string to check

    Returns:
        bool: True if it looks like a DOI/identifier, False if it's a URL
    """
    # DOI pattern: starts with 10. followed by numbers/dots/text
    doi_pattern = r'^10\.\d{4,}/[^\s]+$'

    # If it starts with http:// or https://, it's a URL
    if text.strip().startswith(('http://', 'https://')):
        return False

    # If it matches DOI pattern, it's an identifier
    if re.match(doi_pattern, text.strip()):
        return True

    # Other identifiers like PMID, ISBN, etc. would go here
    # For now, treat anything without http(s) as an identifier
    return not text.strip().startswith(('http://', 'https://'))


def fetch_zotero_citation(input_text):
    """
    Fetch citation metadata from Zotero Translator Server

    Args:
        input_text: URL or identifier (DOI, etc.) to fetch citation data for

    Returns:
        dict: Response from the API or error details
    """
    try:
        # Get credentials from Streamlit secrets (Cloud) or environment variables (local)
        # Streamlit secrets take precedence
        try:
            api_url = st.secrets["zotero"]["api_url"]
            api_key = st.secrets["zotero"]["api_key"]
        except (KeyError, FileNotFoundError):
            # Fall back to environment variables for local development
            api_url = os.getenv('ZOTERO_API_URL')
            api_key = os.getenv('ZOTERO_API_KEY')

        if not api_url or not api_key:
            return {
                "success": False,
                "error": "Zotero API credentials not configured. Please set credentials in .streamlit/secrets.toml (Cloud) or .env file (local).",
            }

        # Determine which endpoint to use
        if is_doi_or_identifier(input_text):
            endpoint = f"{api_url.rstrip('/')}/search"
            endpoint_type = "search"
        else:
            endpoint = f"{api_url.rstrip('/')}/web"
            endpoint_type = "web"

        # Set headers
        headers = {
            "x-api-key": api_key,
            "Content-Type": "text/plain"
        }

        # Make the API call
        response = requests.post(endpoint, headers=headers, data=input_text, timeout=10)

        # Raise exception for bad status codes
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        return {
            "success": True,
            "data": data,
            "endpoint_type": endpoint_type,
            "api_url": endpoint,
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection error. Please check your internet connection.",
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text if hasattr(e.response, 'text') else str(e)
        return {
            "success": False,
            "error": f"HTTP error: {e.response.status_code} - {error_detail}",
        }
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}


def main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="Citation Metadata Fetcher", page_icon="📚", layout="wide"
    )

    # Title and description
    st.title("📚 Citation Metadata Fetcher")
    st.markdown(
        """
    Compare citation metadata from Wikipedia's [Citoid API](https://www.mediawiki.org/wiki/Citoid)
    and your Zotero Translator Server deployment.
    """
    )

    # Comparison mode toggle
    comparison_mode = st.checkbox(
        "🔬 Enable Comparison Mode",
        value=False,
        help="Fetch citations from both Citoid and Zotero Translator Server side-by-side"
    )

    # Example URLs
    with st.expander("📋 Example URLs and DOIs to try"):
        st.markdown("**URLs:**")
        st.code("https://www.nature.com/articles/nature12373", language=None)
        st.code("https://kevinmunger.substack.com/p/towards-the-post-naive-internet", language=None)
        st.code("https://github.com/cosmik-network/semble", language=None)
        st.code("https://arxiv.org/abs/2301.00001", language=None)
        st.markdown("**DOIs (for search endpoint):**")
        st.code("10.2307/4486062", language=None)
        st.code("10.1038/nature12373", language=None)

    # Create two columns for input
    col1, col2 = st.columns([3, 1])

    with col1:
        # URL or DOI input
        url_input = st.text_input(
            "Enter URL or DOI",
            placeholder="https://example.com or 10.1234/example",
            help="Enter a URL or DOI to fetch citation metadata for",
        )

    with col2:
        # Format selector
        format_type = st.selectbox(
            "Citation Format",
            options=["zotero", "mediawiki", "mediawiki-basefields", "bibtex"],
            help="Choose the citation format to retrieve",
        )

    # Fetch button
    if st.button("🔍 Fetch Citation", type="primary"):
        if not url_input:
            st.warning("⚠️ Please enter a URL or DOI")
        else:
            if comparison_mode:
                # Comparison mode: fetch from both APIs
                st.markdown("---")
                col_left, col_right = st.columns(2)

                with col_left:
                    st.subheader("🌐 Citoid API")
                    with st.spinner("Fetching from Citoid..."):
                        citoid_result = fetch_citation(url_input, format_type)

                    if citoid_result["success"]:
                        st.success("✅ Success")
                        with st.expander("🔗 API Request Details"):
                            st.code(citoid_result["api_url"], language="text")

                        if citoid_result["is_json"]:
                            st.json(citoid_result["data"])
                            json_str = json.dumps(citoid_result["data"], indent=2)
                            st.download_button(
                                label="📥 Download JSON",
                                data=json_str,
                                file_name=f"citoid_{citoid_result['format_type']}.json",
                                mime="application/json",
                                key="citoid_download"
                            )
                        else:
                            st.code(citoid_result["data"], language="bibtex")
                            st.download_button(
                                label="📥 Download BibTeX",
                                data=citoid_result["data"],
                                file_name="citoid_citation.bib",
                                mime="text/plain",
                                key="citoid_download"
                            )
                    else:
                        st.error(f"❌ Error: {citoid_result['error']}")

                with col_right:
                    st.subheader("⚡ Zotero Translator Server")
                    with st.spinner("Fetching from Zotero..."):
                        zotero_result = fetch_zotero_citation(url_input)

                    if zotero_result["success"]:
                        st.success(f"✅ Success (via /{zotero_result['endpoint_type']})")
                        with st.expander("🔗 API Request Details"):
                            st.code(zotero_result["api_url"], language="text")

                        st.json(zotero_result["data"])
                        json_str = json.dumps(zotero_result["data"], indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name="zotero_citation.json",
                            mime="application/json",
                            key="zotero_download"
                        )
                    else:
                        st.error(f"❌ Error: {zotero_result['error']}")

            else:
                # Single mode: fetch from Citoid only (original behavior)
                with st.spinner("Fetching citation metadata..."):
                    result = fetch_citation(url_input, format_type)

                if result["success"]:
                    st.success("✅ Citation metadata retrieved successfully!")

                    # Display the API URL used
                    with st.expander("🔗 API Request Details"):
                        st.code(result["api_url"], language="text")

                    # Display the response based on format type
                    st.subheader("Citation Metadata")

                    if result["is_json"]:
                        # Display JSON formats (zotero, mediawiki, mediawiki-basefields)
                        st.json(result["data"])

                        # Download button for JSON
                        json_str = json.dumps(result["data"], indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"citation_{result['format_type']}.json",
                            mime="application/json",
                        )
                    else:
                        # Display text formats (bibtex)
                        st.code(result["data"], language="bibtex")

                        # Download button for text
                        st.download_button(
                            label="📥 Download BibTeX",
                            data=result["data"],
                            file_name="citation.bib",
                            mime="text/plain",
                        )
                else:
                    st.error(f"❌ Error: {result['error']}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: gray;'>
        <small>Powered by <a href='https://www.mediawiki.org/wiki/Citoid'>Wikipedia Citoid API</a> &
        <a href='https://github.com/cosmik-network/zotero-translator-server'>Zotero Translator Server</a> |
        Built with <a href='https://streamlit.io'>Streamlit</a></small>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
