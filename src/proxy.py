from fastapi import Request, HTTPException
from fastapi.responses import Response

from settings import ProxySettings
from utils import modify_url, modify_html


async def get_response(request: Request) -> Response:
    request_headers = prepare_request_headers(dict(request.headers))
    url = f'https://{ProxySettings.DOMAIN}{request.url.path}'
    try:
        async with request.app.state.client_session.request(
            method=request.method,
            url=url,
            params=dict(request.query_params),
            headers=request_headers,
            allow_redirects=True
        ) as habr_response:
            content = await habr_response.read()

            response_headers = prepare_response_headers(dict(habr_response.headers), str(request.base_url))
            if habr_response.content_type == 'text/html':
                text = content.decode('utf8')
                text = modify_html(text, str(request.base_url))
                content = text.encode('utf8')

            response = Response(
                content,
                status_code=habr_response.status,
                headers=response_headers,
                media_type=habr_response.content_type
            )
            return response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=503) from e


def prepare_response_headers(headers: dict[str, str], proxy_address: str) -> dict[str, str]:
    headers.pop('Content-Encoding', None)
    headers.pop('Content-Length', None)
    if location := headers.get('Location'):
        headers['Location'] = modify_url(location, proxy_address)
    return headers


def prepare_request_headers(headers: dict[str, str]) -> dict[str, str]:
    headers['host'] = ProxySettings.DOMAIN
    headers.pop('referer', None)
    headers['connection'] = 'close'
    return headers
