from bs4 import BeautifulSoup

from utils import add_trademark, modify_url, modify_html, modify_attrs


def test_add_trademark() -> None:
    result = add_trademark('Потоки все потоки потоки компании потоки')

    assert result == 'Потоки™ все потоки™ потоки™ компании потоки™'


def test_modify_href() -> None:
    result = modify_url('https://habr.com/reference', 'http://127.0.0.1:8232/')

    assert result == 'http://127.0.0.1:8232/reference'


def test_modify_attrs() -> None:
    soup = BeautifulSoup()
    tag = soup.new_tag('a')
    tag.attrs['href'] = 'https://habr.com/ru/all'

    modify_attrs(tag, 'http://127.0.0.1:8232/', 'href')

    assert tag.attrs['href'] == 'http://127.0.0.1:8232/ru/all'


def test_modify_html() -> None:
    result = modify_html("""<html>
 <head>
  <script>console.log('Все подряд')</script>
  <style>h1{color:silver}</style>
 </head>
 <body>
        <h1>Все потоки</h1>
        <a href="https://habr.com/ru/post/123">Ссылка</a>
        <form action="https://habr.com/search"></form>
        <svg>
            <use xlink:href="https://habr.com/image.png"></use>
        </svg>
    </body>
</html>
            """, 'http://127.0.0.1:8232/')

    assert result == """<html>
 <head>
  <script>
   console.log('Все подряд')
  </script>
  <style>
   h1{color:silver}
  </style>
 </head>
 <body>
  <h1>
   Все потоки™
  </h1>
  <a href="http://127.0.0.1:8232/ru/post/123">
   Ссылка™
  </a>
  <form action="http://127.0.0.1:8232/search">
  </form>
  <svg>
   <use xlink:href="http://127.0.0.1:8232/image.png">
   </use>
  </svg>
 </body>
</html>"""
