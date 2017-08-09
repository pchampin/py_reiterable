============
 Reiterable
============

This module provides the ``reiterable`` function,
which wraps any iterable into a multi-usage iterable.

This is useful, because many iterable can only be iterated over once,
as the values they yield are "consumed" by the iteration.

The ``reiterable`` function tries to be as thrifty as possible.
If the passed iterable looks like it is already multi-usage,
it will return it unchanged.
Otherwise,
it will lazily build a cache of the values yielded by the passed iterable,
and that cache will be shared by all iterators on that object.
