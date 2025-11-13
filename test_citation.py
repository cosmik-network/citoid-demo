"""
Simple test script to verify the citation fetcher functionality
without requiring Streamlit to be installed
"""

import requests
from urllib.parse import quote


def fetch_citation(url, format_type="zotero"):
    """
    Fetch citation metadata from Citoid API

    Args:
        url: The URL to fetch citation data for
        format_type: Citation format (mediawiki, mediawiki-basefields, zotero, bibtex)

    Returns:
        dict: JSON response from the API or error details
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

        # Return JSON response
        return {
            'success': True,
            'data': response.json(),
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


if __name__ == "__main__":
    print("Testing Citation Fetcher...")
    print("-" * 50)

    # Test with a Wikipedia URL
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    print(f"\nTesting with URL: {test_url}")

    result = fetch_citation(test_url, 'zotero')

    if result['success']:
        print("✓ API call successful!")
        print(f"✓ API URL: {result['api_url']}")
        print(f"✓ Retrieved {len(result['data'])} citation record(s)")

        if isinstance(result['data'], list) and len(result['data']) > 0:
            citation = result['data'][0]
            print(f"\nCitation Details:")
            print(f"  - Title: {citation.get('title', 'N/A')}")
            print(f"  - Type: {citation.get('itemType', 'N/A')}")
            print(f"  - URL: {citation.get('url', 'N/A')}")
        print("\n✓ All tests passed!")
    else:
        print(f"✗ API call failed: {result['error']}")
        print("\nNote: This might fail if there's no internet connection.")

    print("-" * 50)
