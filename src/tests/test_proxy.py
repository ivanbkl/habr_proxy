from proxy import prepare_response_headers, prepare_request_headers
from settings import ProxySettings


def test_prepare_response_headers() -> None:
    result = prepare_response_headers({
        'Content-Length': '256',
        'Content-Encoding': 'gzip',
        'Location': 'https://habr.com/ru/all'
    }, 'http://127.0.0.1:8232/')

    assert result == {
        'Location': 'http://127.0.0.1:8232/ru/all'
    }


def test_prepare_request_headers() -> None:
    result = prepare_request_headers({
        'host': '127.0.0.1:8232',
        'referer': 'http://127.0.0.1:8232/',
        'connection': 'keep-alive'
    })

    assert result == {
        'host': ProxySettings.DOMAIN,
        'connection': 'close',
        'cookie': 'web_override=false;'
    }
