from django.urls import path
from .views import ListRepositories, InviteCollaborator, RemoveCollaborator, RevokeAllAccess

urlpatterns = [
    path('Listrepos/', ListRepositories.as_view(), name='list-repositories'),
    path('inviteCollab/', InviteCollaborator.as_view(), name='invite-collaborator'),
    path('removeCollab/', RemoveCollaborator.as_view(), name='remove-collaborator'),
    path('revokeAllAcc/', RevokeAllAccess.as_view(), name='revoke-all-access'),
]
