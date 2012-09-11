import copy
from experimental import helpertools


def source_to_request(source, callback=None, count=None, index=None, reverse=None):
    r'''.. versionadded:: 1.0

    Change request `source` to request object.

    If `source` is one of ... ::

        StatalServer Handler

    ... then return ... ::

        StatalServerRequest
        HandlerRequest

    ... as output.

    If `source` is a constant then return `source` unchanged.

    If `source` is already a request then set `callback`, `count`, `index`
    or `reverse` against `source` (if any are not none) and return `source`.
    '''
    from experimental import handlertools
    from experimental import requesttools
    from experimental import statalservertools

    assert isinstance(callback, (helpertools.Callback, type(None))), repr(callback)
    assert isinstance(count, (int, type(None))), repr(count)
    assert isinstance(index, (int, type(None))), repr(index)

    if isinstance(source, requesttools.Request):
        request = copy.copy(source)
        if callback is not None:
            request.callback = callback
        if count is not None:
            request.count = count
        if index is not None:
            request.index = index
        if reverse is not None:
            request.reverse = reverse
    elif isinstance(source, statalservertools.StatalServer):
        if count is not None or index is not None or reverse is not None:
            request = requesttools.StatalServerRequest(
                source, count=count, index=index, reverse=reverse)
    elif isinstance(source, handlertools.Handler):
        if index is not None:
            assert count is None
            request = requesttools.HandlerRequest(source, index=index)
    elif any([x is not None for x in (callback, count, index, reverse)]):
        raise ValueError(
            "'callback', 'count', 'index' or 'reverse' set on stateless source: {!r}.".format(source))
    else:
        request = source

    return request
