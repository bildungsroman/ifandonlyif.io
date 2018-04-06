from rest_framework import serializers

# the right way to import from another app! (ignore Pycharm's griping)
from ifftasks.models import IffList, TodoItem
from iffapp.users.models import User


class IffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IffList
        owner = serializers.ReadOnlyField(source='IffList.user.username')
        fields = '__all__'


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        owner = serializers.ReadOnlyField(source='user.username')
        fields = '__all__'
        depth = 1
