from contextlib import contextmanager
import codecs

from hypergen.core import *
from hypergen.contrib import hypergen_view, hypergen_callback, NO_PERM_REQUIRED

from django.templatetags.static import static

# Templates - as your app grows you probably want to move them to a templates.py file.

@contextmanager  # base templates must be context managers that yields where the main content will be.
def base_template():
    """
    This base template is meant to be shared between your views.
    """
    doctype()
    with html():
        with head():
            if title:
                title("Hello {{ project_name }}")
            script(src=static("hypergen/hypergen.min.js"))
            link("https://unpkg.com/simpledotcss@2.0.7/simple.min.css")
        with body():  # warning, don't set the id here, does not work!
            h1("Hello {{ project_name }}")
            p(mark("Congratulations on running your very first Django Hypergen Project!"))

            with div(id_="content"):  # see target_id below.
                # The html triggered inside your views will appear here.
                yield
            h1("Where to go from here?")
            with ul():
                li("Play around with the source at", code("./hypergen_first_app/views.py"), sep=" ")
                li("Check out the ", a("documentation", href="https://hypergen.it/documentation/"), ".", sep=" ")
                li("Go crazy 24/7!")

def content_template(encrypted_message=None):
    """
    This template is specific to your view and the callbacks belonging to it.
    """
    p("Top secret agent? Encrypt your message with a super secret key:")
    input_(id_="message", oninput=callback(my_callback, THIS))  # call "my_callback" on each oninput event.
    pre(code(encrypted_message if encrypted_message else "Type something, dammit!"))

# Views - one view is normally an entire app with callbacks as actions.

@hypergen_view(perm=NO_PERM_REQUIRED, base_template=base_template)
def my_view(request):
    """
    Views renders html.
    """
    content_template()

# Callbacks - if you have a lot, move them to a callbacks.py file.

@hypergen_callback(perm=NO_PERM_REQUIRED, target_id="content")
def my_callback(request, message):
    """
    Tells the frontend to put the output of content_template into the 'content' div.
    """
    content_template(codecs.encode(message if message is not None else "", 'rot_13'))
