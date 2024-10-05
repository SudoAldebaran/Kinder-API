from django.urls import path

#doc IMPORT VIEWS
from .views import ParentList, ParentDetail, ChildrenParentsList, ChildList, ChildDetail, HouseholdList, InvitationList, InvitationDetail, AcceptInvitationView

urlpatterns = [
    #doc PARENTS URL
    path('parents/', ParentList.as_view()),
    path('parents/<int:pk>/', ParentDetail.as_view()),

    #doc ALL CHILDREN BY PARENT
    path('parents/<int:pk>/children/', ChildrenParentsList.as_view()),

    #doc CHILDREN URL
    path('children/', ChildList.as_view()),
    path('children/<int:pk>/', ChildDetail.as_view()),

    #doc HOUSEHOLD LIST
    path('household/', HouseholdList.as_view()), #doc HOUSEHOLD URL

    #doc INVITATIONS URL
    path('invitations/', InvitationList.as_view()), #doc INVITATIONS URL
    path('invitations/<int:pk>/', InvitationDetail.as_view()), #doc SPECIFIC INVITATION DETAIL
    path('invitations/<int:pk>/accept/', AcceptInvitationView().as_view()) #doc ACCEPT INVITATION
]