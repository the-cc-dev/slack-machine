import re
import pytest
from machine.plugins.decorators import process, listen_to, respond_to


@pytest.fixture
def process_f():
    @process(event_type='test_event')
    def f(event):
        pass

    return f


@pytest.fixture
def listen_to_f():
    @listen_to(r'hello', re.IGNORECASE)
    def f(msg):
        pass

    return f


@pytest.fixture
def respond_to_f():
    @respond_to(r'hello', re.IGNORECASE)
    def f(msg):
        pass

    return f


@pytest.fixture
def multi_decorator_f():
    @respond_to(r'hello', re.IGNORECASE)
    @listen_to(r'hello', re.IGNORECASE)
    def f(msg):
        pass

    return f


def test_process(process_f):
    assert hasattr(process_f, 'metadata')
    assert 'plugin_actions' in process_f.metadata
    assert 'process' in process_f.metadata['plugin_actions']
    assert 'event_type' in process_f.metadata['plugin_actions']['process']
    assert process_f.metadata['plugin_actions']['process']['event_type'] == 'test_event'


def test_listen_to(listen_to_f):
    assert hasattr(listen_to_f, 'metadata')
    assert 'plugin_actions' in listen_to_f.metadata
    assert 'listen_to' in listen_to_f.metadata['plugin_actions']
    assert 'regex' in listen_to_f.metadata['plugin_actions']['listen_to']
    assert listen_to_f.metadata['plugin_actions']['listen_to']['regex'] == re.compile(r'hello',
                                                                                      re.IGNORECASE)


def test_respond_to(respond_to_f):
    assert hasattr(respond_to_f, 'metadata')
    assert 'plugin_actions' in respond_to_f.metadata
    assert 'respond_to' in respond_to_f.metadata['plugin_actions']
    assert 'regex' in respond_to_f.metadata['plugin_actions']['respond_to']
    assert respond_to_f.metadata['plugin_actions']['respond_to']['regex'] == re.compile(r'hello', re.IGNORECASE)


def test_mulitple_decorators(multi_decorator_f):
    assert hasattr(multi_decorator_f, 'metadata')
    assert 'plugin_actions' in multi_decorator_f.metadata
    assert 'respond_to' in multi_decorator_f.metadata['plugin_actions']
    assert 'listen_to' in multi_decorator_f.metadata['plugin_actions']
    assert 'process' not in multi_decorator_f.metadata['plugin_actions']
