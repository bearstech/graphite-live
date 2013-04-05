Graphite-live
=============

Simple graphite frontend for exposing some features like :
 * Exposing value as event source, no more violent polling
 * Filtering data with path

Test it
-------

Install it

    virtualenv .
    source bin/activate
    pip install -r requirements.txt

Launch it

    python src/web.py htttp://toto.com/toto.json

In some other terminals

    curl http://localhost:8888/


Licence
=======

3 term BSD Licence, © 2013 Mathieu Lecarme.
