"""
Streamlit Citation Metadata Fetcher
Uses Wikipedia's Citoid API to fetch citation metadata for any URL
"""

import streamlit as st
import requests
from urllib.parse import quote
import json


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
        encoded_url = quote(url, safe='')

        # Build the API endpoint
        api_url = f"https://en.wikipedia.org/api/rest_v1/data/citation/{format_type}/{encoded_url}"

        # Set headers with User-Agent
        headers = {
            'User-Agent': 'Streamlit-Citation-Fetcher/1.0 (Educational Project)'
        }

        # Make the API call
        response = requests.get(api_url, headers=headers, timeout=10)

        # Raise exception for bad status codes
        response.raise_for_status()

        # Parse response based on format type
        # BibTeX returns plain text, others return JSON
        if format_type == 'bibtex':
            data = response.text
            is_json = False
        else:
            data = response.json()
            is_json = True

        return {
            'success': True,
            'data': data,
            'is_json': is_json,
            'format_type': format_type,
            'api_url': api_url
        }

    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Connection error. Please check your internet connection.'
        }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out. Please try again.'
        }
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP error: {e.response.status_code} - {e.response.reason}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'An unexpected error occurred: {str(e)}'
        }


def main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="Citation Metadata Fetcher",
        page_icon="📚",
        layout="wide"
    )

    # Title and description
    st.title("📚 Citation Metadata Fetcher")
    st.markdown("""
    This app uses Wikipedia's [Citoid API](https://www.mediawiki.org/wiki/Citoid) to fetch
    citation metadata for any URL. Simply enter a URL below and click "Fetch Citation" to get started.
    """)

    # Example URLs
    with st.expander("📋 Example URLs to try"):
        st.markdown("""
        - `https://www.nature.com/articles/nature12373`
        - `https://arxiv.org/abs/1706.03762`
        - `https://en.wikipedia.org/wiki/Artificial_intelligence`
        - `https://www.bbc.com/news/technology-12345678`
        - `https://github.com/streamlit/streamlit`
        """)

    # Create two columns for input
    col1, col2 = st.columns([3, 1])

    with col1:
        # URL input
        url_input = st.text_input(
            "Enter URL",
            placeholder="https://example.com",
            help="Enter the URL you want to fetch citation metadata for"
        )

    with col2:
        # Format selector
        format_type = st.selectbox(
            "Citation Format",
            options=["zotero", "mediawiki", "mediawiki-basefields", "bibtex"],
            help="Choose the citation format to retrieve"
        )

    # Fetch button
    if st.button("🔍 Fetch Citation", type="primary"):
        if not url_input:
            st.warning("⚠️ Please enter a URL")
        else:
            # Show loading spinner
            with st.spinner("Fetching citation metadata..."):
                result = fetch_citation(url_input, format_type)

            if result['success']:
                st.success("✅ Citation metadata retrieved successfully!")

                # Display the API URL used
                with st.expander("🔗 API Request Details"):
                    st.code(result['api_url'], language="text")

                # Display the response based on format type
                st.subheader("Citation Metadata")

                if result['is_json']:
                    # Display JSON formats (zotero, mediawiki, mediawiki-basefields)
                    st.json(result['data'])

                    # Download button for JSON
                    json_str = json.dumps(result['data'], indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name=f"citation_{result['format_type']}.json",
                        mime="application/json"
                    )
                else:
                    # Display text formats (bibtex)
                    st.code(result['data'], language="bibtex")

                    # Download button for text
                    st.download_button(
                        label="📥 Download BibTeX",
                        data=result['data'],
                        file_name="citation.bib",
                        mime="text/plain"
                    )
            else:
                st.error(f"❌ Error: {result['error']}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <small>Powered by <a href='https://www.mediawiki.org/wiki/Citoid'>Wikipedia Citoid API</a> |
        Built with <a href='https://streamlit.io'>Streamlit</a></small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
