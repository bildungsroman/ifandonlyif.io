from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView

from ifftasks.models import IffList, TodoItem  # the right way to import from another app! (ignore Pycharm's griping)
from .models import User


def home(request):
    """Renders the homepage view when a user is logged in"""
    user_lists = IffList.objects.filter(user=request.user,  # get only the ifflists of logged-in user
                                        is_completed=False)  # get all of a user's ifflists that are not completed
    context = {'user_lists': user_lists}
    return render(request, 'pages/home.html', context)


class IfflistInfoMixin (object):
    """to be used throughout the app to provide ifflist data"""
    def get_context_data(self, **kwargs):
        context = super(IfflistInfoMixin, self).get_context_data(**kwargs)

        ... # Add more to context object


class UserCreateView(LoginRequiredMixin, IfflistInfoMixin, CreateView):
    """this will be for creating and saving new ifflists"""
    model = User

    def create_new_ifflist(self):
        pass


class UserDetailView(LoginRequiredMixin, IfflistInfoMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'user_bio', 'user_goals', 'profile_pic']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
