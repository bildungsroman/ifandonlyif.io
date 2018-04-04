from django.db import models
from django.utils import timezone
from django.dispatch import receiver
# from ..users.models import User  # this doesn't compile :(
from iffapp.users.models import User


class IffList(models.Model):
    """
    The main ifflist item, with one required get-to-do and unlimited TodoItem items
    """
    get_to_do = models.CharField(max_length=200)  # the one get to do item
    get_to_do_available = models.BooleanField(default=False)  # can you do the get-to-do
    get_to_do_is_completed = models.BooleanField(default=False)  # is the get-to-do completed
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # if user deleted, delete all user's lists
    created_date = models.DateTimeField(auto_now_add=True)  # automatically added, for sorting on homepage view
    completed_date = models.DateTimeField(null=True, blank=True)  # add IFFlist to archive upon completion
    is_completed = models.BooleanField(default=False)  # is this whole list completed, including get-to-do?
    # this way we can do current_tasks = IffList.objects.filter(is_completed=False)
    # or current_tasks = IffList.objects.filter(is_completed=True)
    # in views to show current and completed items separately

    # complete the ifflist
    def complete(self):
        if self.get_to_do_is_completed is True:
            self.is_completed = True

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
    ifflist = models.ForeignKey(IffList,  # which list this item belongs to - assign in detail view
                                on_delete=models.CASCADE,  # if list deleted, delete all list items
                                related_name='item')  # use this name instead of todoitem
    is_completed = models.BooleanField(default=False)  # is this item completed

    # this way we can do check off items in the detail view
    def complete(self):  # runs from detail template
        self.is_completed = True

    @classmethod
    def create_welcome_todos(cls, text, ifflist):
        # create a default welcome list
        new_todo = cls(text=text, ifflist=ifflist)
        return new_todo

    def __str__(self):
        return self.text


# create a 'welcome' list upon user creation
# @receiver(models.signals.post_save, sender=User)
def create_first_ifflist(sender, instance, created, **kwargs):
    if created:
        # create a new welcome IFFlist for the user with three to-dos
        welcome_list = IffList(get_to_do="party like it's 1999!", user=instance)
        welcome_list.save()
        welcome_todo1 = TodoItem.create_welcome_todos("complete my profile", welcome_list)
        welcome_todo1.save()
        welcome_todo2 = TodoItem.create_welcome_todos("add my first ifflist", welcome_list)
        welcome_todo2.save()
        welcome_todo3 = TodoItem.create_welcome_todos("tell my friends about IFF", welcome_list)
        welcome_todo3.save()


models.signals.post_save.connect(create_first_ifflist, sender=User)
