from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.browse_ventures, name='list'),
    path('favorites/', views.display_saved_ventures, name='favorites'),
    path('create-project/', views.publish_venture, name='create'),
    path('<int:pk>/edit/', views.amend_venture, name='edit'),
    path('<int:pk>/', views.display_venture_detail, name='detail'),
    path('<int:pk>/toggle-favorite/', views.flip_bookmark_state, name='toggle_favorite'),
    path('<int:pk>/complete/', views.finalize_venture, name='complete'),
    path('<int:pk>/toggle-participate/', views.flip_membership_state, name='toggle_participate'),
]
