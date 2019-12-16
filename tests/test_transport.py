from mock import MagicMock, patch, call

from pypodio2.transport import _retry, TransportException
from tests.utils import get_client_and_http


@patch('time.sleep')
def retry_helper(tries, delay, backoff, cap, mock_sleep):
    """
    Helper function that calls a function with the retry decorator. This
    helper returns mock_request and mock_sleep. mock_request is called from
    inside the decorated function, and mock_sleep is the mocked `time.sleep`.
    """
    mock_request = MagicMock()
    mock_status = MagicMock()
    mock_status.status = 502

    @_retry(tries, delay, backoff, cap)
    def func():
        mock_request()
        raise TransportException(mock_status, None)

    # The function should eventually raise the exception
    try:
        func()
    except TransportException:
        pass
    else:
        raise AssertionError()

    return mock_request, mock_sleep


def test_retry():
    """
    Check that the function is executed the correct amount of times and that
    the sleep times are also correct.
    """
    mock_request, mock_sleep = retry_helper(3, 2, 2, 10)
    assert mock_request.call_count == 3
    assert mock_sleep.call_count == 2

    mock_request, mock_sleep = retry_helper(4, 5, 4, 100)
    assert mock_request.call_count == 4
    assert mock_sleep.call_count == 3


def test_retry_disabled():
    """The decorator shouldn't retry when tries, delay or backoff are None."""
    mock_request, mock_sleep = retry_helper(3, None, 2, 10)
    assert mock_request.call_count == 1
    assert mock_sleep.call_count == 0


def test_retry_sleep_calc():
    retries = 10000
    base_delay = 2
    backoff = 2
    cap = 3600
    retry = _retry(retries, base_delay, backoff, cap)
    for attempt in range(retries):
        calc_delay = retry._calc_delay(attempt)
        max_delay = min(cap, base_delay * backoff ** attempt)
        assert 0 <= calc_delay <= max_delay


@patch('time.sleep')
def test_transport(mock_sleep):
    mock_status = MagicMock()
    mock_status.status = 502

    client, _ = get_client_and_http()
    client.setup_retry(3, 2, 2, 10)
    client.transport._http.request = MagicMock(side_effect=TransportException(mock_status, None))

    try:
        client.Contact.get_contacts()
    except TransportException:
        pass
    else:
        raise AssertionError()

    assert client.transport._http.request.call_count == 3
    assert mock_sleep.call_count == 2
