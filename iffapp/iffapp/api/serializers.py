from rest_framework import serializers

# the right way to import from another app! (ignore Pycharm's griping)
from ifftasks.models import IffList, TodoItem
from iffapp.users.models import User


class IffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IffList
        owner = serializers.ReadOnlyField(source='IffList.user.username')
        fields = ['get_to_do', 'get_to_do_available', 'get_to_do_is_completed', 'user', 'created_date', 'completed_date', 'is_completed', 'id']


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['text', 'ifflist', 'is_completed', 'id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        owner = serializers.ReadOnlyField(source='user.username')
        fields = ['name', 'is_new_user', 'profile_pic', 'user_bio', 'user_goals', 'friends_with', 'number_of_lists', 'premium_account', 'id']
