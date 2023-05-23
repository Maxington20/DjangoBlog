from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_post/', views.generate_post, name='generate_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('send_message/', views.send_message, name='send_message'),  # Add this line

]