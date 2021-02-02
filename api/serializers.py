from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user', 'place')
        # fields = '__all__'  