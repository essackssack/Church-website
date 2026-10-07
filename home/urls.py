from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('branches/', views.branches, name='branches'),
    path('events/', views.events, name='events'),
    path('magazine/', views.magazine, name='magazine'),
    path('music/', views.music, name='music'),
    path('music/new-songs/', views.new_songs, name='new_songs'),
    path('media/', views.media, name='media'),
    path('community/', views.community, name='community'),
    path('contact/', views.contact, name='contact'),
    path(
        'sections/<slug:main_heading>/<slug:subheading>/',
        views.subheading_detail,
        name='subheading_detail',
    ),
    path('search/', views.coming_soon, {'page_name': 'Search'}, name='search'),
]
