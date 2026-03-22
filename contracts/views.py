from django.shortcuts import render
from rest_framework import viewsets
from contracts.serializers import ContractSerializer
from contracts.models import Contract

# Create your views here.
class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all().order_by('id')
