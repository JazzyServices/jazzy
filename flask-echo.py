"""Simple Flask app that echoes the request that it is sent.

MIT License

Copyright (c) 2018 Jazzy Services Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Usage:
1. launch the app ...
    python flask-echo.py &
2. fire requests at it, e.g.
    curl "http://0.0.0.0:5000/echo?beach=sandy&sea=wet"
    curl -d "beach=sandy&sea=wet" http://0.0.0.0:5000/echo
    curl -F 'source=@echo.py;type=text/plain' http://0.0.0.0:5000/echo
    curl -u bob:passwd http://0.0.0.0:5000/echo
"""
import collections
import werkzeug

import flask
app = flask.Flask(__name__)


def transtype(obj):
    """Translate an object into a JSONable type."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        # JSON-safe
        return obj
    elif isinstance(obj, bytes):
        return obj.decode('latin-1')
    elif isinstance(obj, (list, tuple, set)):
        # sequences
        return [transtype(x) for x in obj]
    elif isinstance(obj, (dict, werkzeug.Headers)):
        # dict-a-like classes
        dd = {}
        for kk, vv in obj.items():
            dd[kk] = transtype(vv)
        return dd
    elif isinstance(obj, (werkzeug.Accept, werkzeug.HeaderSet)):
        # list-a-like classes
        return [transtype(x) for x in obj]
    elif isinstance(obj, (
            werkzeug.UserAgent,
            werkzeug.FileStorage,
            werkzeug.routing.Map,
            werkzeug.routing.Rule,
            werkzeug.datastructures.IfRange
    )):
        return dirobj(obj)
    elif hasattr(obj, '__name__'):
        # if it has a name, show its type as well
        return '<%s:%s>' % (obj.__class__.__name__, obj.__name__)
    elif isinstance(obj, collections.Iterable):
        # other iterables might block or might by unsafe
        return '*(%s)' % obj.__class__.__name__
    else:
        # anything else just show the class name
        return '<%s>' % obj.__class__.__name__

def dirobj(req):
    """Show all of the attributes of an object."""
    d = {}
    for k in dir(req):
        # ignore "private" members
        if k[0] == '_':
            continue
        obj = getattr(req, k)
        # filter out unset values
        if obj is None:
            continue
        # ignore functions and methods
        if callable(obj):
            continue
        d[k] = transtype(obj)
    return d

@app.route('/echo', methods=['GET', 'POST', 'PUT'])
def echo():
    d = dirobj(flask.request)
    return flask.jsonify(d)

if __name__ == "__main__":
    app.run()
