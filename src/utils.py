import requests
from requests.adapters import HTTPAdapter, Retry


def fetch_data_with_retries(url: str, params: dict = None):
    """Fetch data from a URL with retries.

    Args:
    - url (str): The URL to fetch data from.
    - params (dict, optional): Dictionary of query parameters.

    Returns:
    - (success, message) Tuple(bool, JSON)
    """

    # Set up retry logic
    retry_strategy = Retry(
        total=5,  # Total retries
        backoff_factor=1,  # Delay between retries: 2s, 4s, 8s, etc.
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on specific status codes
        allowed_methods=["GET"],  # Only retry on GET requests
        raise_on_status=False  # Don't raise exception on status, we'll handle it manually
    )

    # Set up a session with our retry strategy
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    response = session.get(
        url=url,
        params=params,
        timeout=5  # Time in seconds before giving up the request
    )

    if response.status_code == 200:
        return True, response.json()
    else:
        # Return error message for non-successful status codes
        return False, f"Failed with status {response.status_code}: {response.text}"
