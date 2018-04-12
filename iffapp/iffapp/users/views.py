from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView
from django.utils import timezone

from ifftasks.models import IffList, TodoItem  # the right way to import from another app! (ignore Pycharm's griping)
from .models import User


def home(request):
    """Renders the homepage view when a user is logged in"""
    if request.user.is_authenticated:
        # get all of a user's ifflists that are not completed
        user_lists = IffList.objects.filter(user=request.user,  # get only the ifflists of logged-in user
                                            is_completed=False).order_by('-created_date')  # display newest first
        context = {'user_lists': user_lists}
    else:
        # Renders a landing page when a user is not logged in
        context = {}
    return render(request, 'pages/home.html', context)


def save_ifflist(request):
    pass


class IfflistInfoMixin (object):
    """To be used throughout the app to provide ifflist data"""
    def get_context_data(self, **kwargs):
        context = super(IfflistInfoMixin, self).get_context_data(**kwargs)
        context['ifflist_set'] = IffList.objects.all().order_by('-created_date')
        context['todos_set'] = TodoItem.objects.all().order_by('-created_date')
        context['user_ifflists_current'] = IffList.objects.filter(user=self.request.user, is_completed=False).order_by('-created_date')
        context['user_ifflists_completed'] = IffList.objects.filter(user=self.request.user, is_completed=True).order_by('-created_date')
        user_latest_ifflist = IffList.objects.filter(user=self.request.user, is_completed=False).latest('created_date')
        context['user_latest_ifflist'] = user_latest_ifflist
        context['user_latest_todos'] = TodoItem.objects.filter(ifflist=user_latest_ifflist).order_by('-created_date')
        context['timestamp'] = timezone.now()  # need to run this from  Django, not Vue, to get completed_date
        return context


class UserCreateView(LoginRequiredMixin, IfflistInfoMixin, CreateView):
    """This will be for creating and saving new ifflists"""
    model = User


class UserDetailView(LoginRequiredMixin, IfflistInfoMixin, DetailView):
    """This is the main page where user ifflists will be displayed"""
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    # avoid doing this for now...
    # def complete_get_to_do(self, request, *args, **kwargs):  # runs from detail template
    #     for ifflist in IffList.objects.filter(user=self.request.user, is_completed=False):
    #         if ifflist.get_to_do_is_completed is True:
    #             ifflist.completed_date = timezone.now()  # need to run this from  Django to get completed_date
    #             ifflist.is_completed = True
    #             ifflist.save()
    #             print("Completed ifflist from view ID: ", ifflist.id)
    #             return super().dispatch(request, *args, **kwargs)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update the user profile (for the sidebar)"""
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
    """Not being user right now, may be used in the future to show a user's friends"""
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
