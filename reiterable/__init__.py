"""
I provide the :func:`reiterable` function.
"""
import threading
import sys

__version__ = "0.1.0"

def reiterable(it, thread_safe=False, force=False):
    """
    I wrap any iterable into a multi-usage iterable.

    This means that the returned value can be iterated over multiple times,
    and will produce the same result each time.

    Of course, ``it`` should not be iterated over after being passed to this function,
    as its internal state may be altered by the iterable returned by this function.

    Note that the returned iterable is not thread-safe by default;
    it is possible to make it so with the ``thread_safe`` argument.

    Note also that only objects that verify ``iter(it) is it`` are actually wrapped
    by this functions (this is the case of all native *iterators*).
    Other iterable objects (those such that ``iter(it) is not it``) are assumed to be
    already reiterable, and are returned as is.
    This assumption is verified by built-in types (such as list, tuple, dict...)
    but may be violated by exotic classes...
    """
    if iter(it) is not it:
        # it is an iterable, not an iterator
        # so it needs no wrapping (unless forced)
        if not force:
            return it
        else:
            it = iter(it)
    # it is an iterator, we must wrap it
    if thread_safe:
        return _ReiterableWrapperTS(it)
    else:
        return _ReiterableWrapper(it)


class _ReiterableWrapper(object):
    def __init__(self, it):
        self._it = it
        self._start = []

    def __iter__(self):
        return _ReiterableIterator(self)

class _ReiterableIterator(object):
    def __init__(self, wrapper):
        self._wrapper = wrapper
        self._next = 0

    def __next__(self):
        _start = self._wrapper._start
        if self._next >= len(_start):
            assert self._next == len(_start) # else, how would have reached this index?
            _start.append(next(self._wrapper._it))
        ret = _start[self._next]
        self._next += 1
        return ret

    if sys.version_info.major < 3:
        def next(self):
            return self.__next__()


class _ReiterableWrapperTS(_ReiterableWrapper):
    def __iter__(self):
        return _ReiterableIteratorTS(self)

class _ReiterableIteratorTS(_ReiterableIterator):
    """A thread-safe variant of _ReiterableIterator"""
    def __init__(self, wrapper):
        _ReiterableIterator.__init__(self, wrapper)
        self._lock = threading.Lock()

    def __next__(self):
        with self._lock:
            return _ReiterableIterator.__next__(self)
    
