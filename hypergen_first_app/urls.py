from hypergen.hypergen import autourls
from hypergen_first_app import views

app_name = 'hypergen_first_app'

# Automatically creates urlpatterns for all functions in views.py decorated with @liveview or
# @action.
urlpatterns = autourls(views, namespace="hypergen_first_app")
