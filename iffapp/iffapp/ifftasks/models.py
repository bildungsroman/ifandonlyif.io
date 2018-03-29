from django.db import models
from django.utils import timezone
# from ..users.models import User  # this doesn't compile :(
from iffapp.users.models import User


class IffList(models.Model):
    """
    List of ifflist items, including one get-to-do and unlimited to-do items
    """
    get_to_do = models.CharField(max_length=200)  # the one get to do item
    get_to_do_available = models.BooleanField(default=False)  # can you do the get-to-do
    get_to_do_is_completed = models.BooleanField(default=False)  # is the get-to-do completed
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # if user deleted, delete all user's lists
    created_date = models.DateTimeField(auto_now_add=True)  # automatically added, for sorting on homepage view
    completed_date = models.DateTimeField(null=True, blank=True)  # add IFFlist to archive upon completion
    is_completed = models.BooleanField(default=False)  # is this whole list completed, including get-to-do?
    # this way we can do current_tasks = IffList.objects.filter(is_completed=False)
    # or current_tasks = IffList.objects.filter(is_completed=True)
    # in views to show current and completed items separately

    # this way we can do check off the get-to-do in the detail view
    def complete_get_to_do(self):  # runs from detail template
        self.get_to_do_is_completed = True
        self.completed_date = timezone.now()
        self.is_completed = True

    def allow_get_to_do(self):
        # check if all to-dos are completed so get-to-do can be checked off
        for item in self.items.all():
            if not item.is_completed:
                return False
        self.get_to_do_available = True
        return True

    def __str__(self):
        return self.get_to_do


class TodoItem(models.Model):
    """
    The main model for individual IFFlist to-do items
    """
    text = models.CharField(max_length=200)  # this is the text of the actual to-do
    ifflist = models.ForeignKey(IffList, on_delete=models.CASCADE, related_name='items')
    # if list deleted, delete all list items
    # which list this item belongs to - assign in detail view
    is_completed = models.BooleanField(default=False)  # is this item completed

    # this way we can do check off items in the detail view
    def complete(self):  # runs from detail template
        self.is_completed = True

    def __str__(self):
        return self.text
