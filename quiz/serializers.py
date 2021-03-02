from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class TblQuizListSerizlizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TblQuizlist
       	fields = '__all__'

#REFER TO urls.py for rest of the serializers and viewsets
