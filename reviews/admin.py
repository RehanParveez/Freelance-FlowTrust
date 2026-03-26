from django.contrib import admin
from reviews.models import Review, Rating

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
  list_display = ['reviewer', 'reviewee', 'contract', 'milest_submiss', 'comments', 'created_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
  list_display = ['review', 'score', 'quality', 'professionalism'] 

  
