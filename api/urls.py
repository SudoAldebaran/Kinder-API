from django.urls import path

#doc IMPORT VIEWS
from .views import ParentList, ParentDetail, ChildrenParentsList, ChildList, ChildDetail, HouseholdList, InvitationList

urlpatterns = [
    #doc PARENTS URL
    path('parents/', ParentList.as_view()),
    path('parents/<int:pk>/', ParentDetail.as_view()),

    #doc ALL CHILDREN BY PARENT
    path('parents/<int:pk>/children/', ChildrenParentsList.as_view()),


    #doc CHILDREN URL
    path('children/', ChildList.as_view()),
    path('children/<int:pk>/', ChildDetail.as_view()),


    path('household/', HouseholdList.as_view()), #doc HOUSEHOLD URL
    path('invitations/', InvitationList.as_view()), #doc INVITATIONS URL
]