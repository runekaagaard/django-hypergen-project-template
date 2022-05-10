from contextlib import contextmanager
import codecs

from hypergen.core import *
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

# Templates - as you app grows you probably want to move them to a templates.py file.

@contextmanager  # base templates must be context managers that yields where the main content will be.
def base_template():
    """
    This base template is meant to be shared between your views.
    """
    doctype()
    with html():
        with head():
            if title:
                title("Hello {{ app_name }}")
            script(src=static("hypergen/hypergen.min.js"))
            link("https://unpkg.com/simpledotcss@2.0.7/simple.min.css")
        with body():
            h1("Hello {{ app_name }}")
            with div(id_="content"):
                # The html triggered inside your views will appear here.
                yield

def content_template(encrypted_message=None):
    """
    This template is specific to your view and the callbacks belonging to it.
    """
    p("Top secret agent? Encrypt your message with a super secret key:")
    input_(id_="message", oninput=callback(my_callback, THIS))
    pre(code(encrypted_message if encrypted_message else "Type something, dammit!"))

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_template)
def my_view(request):
    content_template()

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="content")
def my_callback(request, message):
    content_template(codecs.encode(message, 'rot_13'))
