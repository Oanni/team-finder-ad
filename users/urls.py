from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.enroll_new_member, name='register'),
    path('login/', views.establish_session, name='login'),
    path('logout/', views.terminate_session, name='logout'),
    path('<int:pk>/', views.display_member_card, name='profile'),
    path('edit-profile/', views.revise_member_profile, name='profile_edit'),
    path('change-password/', views.rotate_credentials, name='change_password'),
    path('list/', views.browse_members, name='user_list'),
]
