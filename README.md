PyPodio
=====

Python wrapper for the Podio API.

Example
-------

```python
from pypodio2 import api
from client_settings import *

client = api.OAuthClient(
    client_id,
    client_secret,
    username,
    password,    
)
print(client.Item.find(22342))
```

Notes
------

It is possible to override the default response handler by passing handler as
a keyword argument to a transport function call. For example:

```python
handler = lambda response, data: (response, data)
response, data = client.Item.find(11007, basic=True, handler=handler)
```

Tests
-----

To run the tests on python 2 & 3:

```
$ tox
```

For quicker tests only with your local interpreter:

```
$ nosetests
```
