from rest_framework import serializers
from reviews.models import Review, Rating

class ReviewSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['reviewer', 'reviewee', 'ratings', 'contract']

class RatingSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Rating
    fields = ['review', 'score']