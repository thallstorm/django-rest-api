from django.urls import path, include
from .views import register_user, user_login, user_logout, change_password, add_skill, remove_skill, create_project, delete_project, express_interest, accept_collaboration, decline_collaboration, user_statistics, open_projects

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('add_skill/', add_skill, name='add_skill'),
    path('remove_skill/<int:skill_id>/', remove_skill, name='remove_skill'),
    path('create_project/', create_project, name='create_project'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('express_interest/<int:project_id>/', express_interest, name='express_interest'),
    path('accept_collaboration/<int:collaboration_id>/', accept_collaboration, name='accept_collaboration'),
    path('decline_collaboration/<int:collaboration_id>/', decline_collaboration, name='decline_collaboration'),
    path('user_statistics/', user_statistics, name='user_statistics'),
    path('open_projects/', open_projects, name='open_projects'),
]