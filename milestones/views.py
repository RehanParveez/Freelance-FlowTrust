from django.shortcuts import render
from rest_framework import viewsets
from milestones.serializers import MilestoneSerializer
from milestones.models import Milestone

# Create your views here.
class MilestoneViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneSerializer
  queryset = Milestone.objects.all().order_by('id')
