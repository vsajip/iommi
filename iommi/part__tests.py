from django.utils.html import format_html
from django.utils.safestring import mark_safe
from tri_struct import Struct

from iommi._web_compat import Template
from iommi.part import (
    as_html,
    request_data,
)
from tests.helpers import req


def test_request_data():
    r = Struct(method='POST', POST='POST', GET='GET')
    assert request_data(r) == 'POST'
    r.method = 'GET'
    assert request_data(r) == 'GET'


def test_as_html():
    # str case
    assert format_html('{}', as_html(part='foo', context={})) == 'foo'
    assert format_html('{}', as_html(part='<foo>bar</foo>', context={})) == '&lt;foo&gt;bar&lt;/foo&gt;'
    assert format_html('{}', as_html(part=mark_safe('<foo>bar</foo>'), context={})) == '<foo>bar</foo>'

    # Template case
    request = req('get')
    assert format_html('{}', as_html(request=request, part=Template('foo'), context={})) == 'foo'
    assert format_html('{}', as_html(request=request, part=Template('<foo>bar</foo>'), context={})) == '<foo>bar</foo>'

    # __html__ attribute case
    assert format_html('{}', as_html(part=Struct(__html__=lambda: 'foo'), context={})) == 'foo'
    assert format_html('{}', as_html(part=Struct(__html__=lambda: '<foo>bar</foo>'), context={})) == '&lt;foo&gt;bar&lt;/foo&gt;'
    assert format_html('{}', as_html(part=Struct(__html__=lambda: mark_safe('<foo>bar</foo>')), context={})) == '<foo>bar</foo>'


def test_as_html_integer():
    assert as_html(part=123, context={}) == '123'
