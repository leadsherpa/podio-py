PyPodio
=====

Python wrapper for the Podio API.

Example
-------

    from pypodio2 import api
    from client_settings import *

    c = api.OAuthClient(
        client_id,
        client_secret,
        username,
        password,    
    )
    print c.Item.find(22342)

Notes
------

It is possible to override the default response handler by passing handler as
a keyword argument to a transport function call. For example:

    x = lambda x,y: (x,y)
    result = c.Item.find(11007, basic=True, handler=x)
    ($result, $data) #Returned info

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
