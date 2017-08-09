import pytest

from reiterable import reiterable

def _iterable_params():
    lst = [1,2,4,5]
    yield lst
    yield tuple(lst)
    yield dict(zip(lst, lst))
    
@pytest.fixture(scope='module', params=_iterable_params())
def iterable(request):
    return request.param

@pytest.fixture(scope='module', params=[False, True])
def thread_safe(request):
    return request.param

def make_gen(last=5):
    yield 1
    yield 2
    yield 4
    yield last

def test_do_not_wrap_iterable(iterable, thread_safe):
    assert iterable is reiterable(iterable, thread_safe)

def test_force_wrap_iterable(iterable, thread_safe):
    reit = reiterable(iterable, thread_safe, force=True)
    assert iterable is not reit
    assert list(iterable) == list(reit)

def test_wrap_generator(thread_safe):
    gen = make_gen()
    reit = reiterable(gen, thread_safe)
    assert reit is not gen
    l1 = list(reit)
    l2 = list(reit)
    l3 = list(make_gen())
    assert l1 is not l2
    assert l2 is not l3
    assert l1 is not l3
    assert l1 == l2
    assert l2 == l3
    assert l1 == l3

def test_only_one_argument():
    gen = make_gen()
    reit = reiterable(gen)
    assert reit is not gen
    l1 = list(reit)
    l2 = list(reit)
    l3 = list(make_gen())
    assert l1 is not l2
    assert l2 is not l3
    assert l1 is not l3
    assert l1 == l2
    assert l2 == l3
    assert l1 == l3
    
