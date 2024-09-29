from django.urls import path

#doc IMPORT VIEWS
from .views import ParentList, ChildList, HouseholdList, InvitationList

urlpatterns = [
    path('parents/', ParentList.as_view()), #doc PARENTS URL
    path('children', ChildList.as_view()), #doc CHILDREN URL
    path('household', HouseholdList.as_view()), #doc HOUSEHOLD URL
    path('invitations', InvitationList.as_view()), #doc INVITATIONS URL
]