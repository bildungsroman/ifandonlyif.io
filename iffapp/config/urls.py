from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from material.frontend import urls as frontend_urls
from allauth.account import views as allauth_views

from iffapp.users import views as user_views  # ignore Pycharm's complaints, this is correct for Django
from iffapp.api import views as api_views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),  # original path
    path('', user_views.home, name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
    path(settings.ADMIN_URL, admin.site.urls),

    # Django Rest Framework API stuff
    path('api/', api_views.IffListCreateAPIView.as_view(), name='ifflist_rest_api'),
    # insecure at the moment, and might be unnecessary
    path('api/todoitems/', api_views.TodoListCreateAPIView.as_view(), name='todoitem_rest_api'),
    path('api/user/', api_views.UserListCreateAPIView.as_view(), name='user_rest_api'),
    # api/:slug
    path('api/<int:id>/', api_views.IffListRetrieveUpdateDestroyAPIView.as_view(), name='ifflist_rest_api'),
    # insecure at the moment
    path('api/todoitems/<int:id>/', api_views.TodoRetrieveUpdateDestroyAPIView.as_view(), name='todoitem_rest_api'),
    path('api/user/<int:id>/', api_views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_rest_api'),

    # User management
    path('user/', include('iffapp.users.urls', namespace='users')),
    # path('accounts/', include('allauth.urls')),  # get rid of the default, replace with custom URLs below:
    path("signup/", allauth_views.signup, name="account_signup"),
    path("login/", allauth_views.login, name="account_login"),
    path("logout/", allauth_views.logout, name="account_logout"),

    path("password/change/", allauth_views.password_change, name="account_change_password"),
    path("password/set/", allauth_views.password_set, name="account_set_password"),

    path("inactive/", allauth_views.account_inactive, name="account_inactive"),

    # E-mail
    path("settings/", allauth_views.email, name="account_email"),
    path("confirm-email/", allauth_views.email_verification_sent, name="account_email_verification_sent"),
    path("confirm-email/<key>", allauth_views.confirm_email, name="account_confirm_email"),

    # password reset
    path("password/reset/", allauth_views.password_reset, name="account_reset_password"),
    path("password/reset/done/", allauth_views.password_reset_done, name="account_reset_password_done"),
    path("password/reset/key/<uidb36><key>", allauth_views.password_reset_from_key, name="account_reset_password_from_key"),
    path("password/reset/key/done/", allauth_views.password_reset_from_key_done, name="account_reset_password_from_key_done"),

    # Your stuff: custom urls includes go here
    path('', include(frontend_urls)),  # material frontend stuff

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
