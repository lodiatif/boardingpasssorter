from django.urls import path, include
from apis import views

urlpatterns = [
    path('sort_trips/', views.sort_trips),

]
