from rest_framework import serializers
from reviews.serializers.basic import RatingSerializer1
from accounts.serializers.basic import UserSerializer1
from contracts.serializers.basic import ContractSerializer1
from reviews.models import Review, Rating

class ReviewSerializer(serializers.ModelSerializer):
  ratings = RatingSerializer1(many=True, read_only=True)
  reviewer = UserSerializer1(read_only=True)
  reviewee = UserSerializer1(read_only=True)
  contract = ContractSerializer1(read_only=True)
  class Meta:
    model = Review
    fields = ['reviewer', 'reviewee', 'ratings', 'contract', 'milest_submiss', 'comments', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rating
    fields = ['review', 'score', 'quality', 'professionalism']
