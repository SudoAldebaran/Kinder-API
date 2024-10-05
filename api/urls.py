from django.urls import path

# doc IMPORT VIEWS
from .views import (
    ParentList,
    ParentDetail,
    ChildrenParentsList,
    ChildList,
    ChildDetail,
    HouseholdList,
    InvitationList,
    InvitationDetail,
    AcceptInvitationView
)

urlpatterns = [
    # doc PARENTS URL
    path(
        'parents/',
        ParentList.as_view(),
        name='parent-list'),
    # doc ADDING NAME FOR THE URL
    path(
        'parents/<int:pk>/',
        ParentDetail.as_view(),
        name='parent-detail'),
    # doc ADDING NAME FOR THE URL

    # doc ALL CHILDREN BY PARENT
    path(
        'parents/<int:pk>/children/',
        ChildrenParentsList.as_view(),
        name='children-parents-list'),
    # doc URL FOR ALL CHILDREN OF A PARENT

    # doc CHILDREN URL
    path(
        'children/',
        ChildList.as_view(),
        name='child-list'),
    # doc ADDING NAME FOR THE URL
    path(
        'children/<int:pk>/',
        ChildDetail.as_view(),
        name='child-detail'),
    # doc ADDING NAME FOR THE URL

    # doc HOUSEHOLD LIST
    path(
        'household/',
        HouseholdList.as_view(),
        name='household-list'),
    # doc ADDING NAME FOR THE URL

    # doc INVITATIONS URL
    path(
        'invitations/',
        InvitationList.as_view(),
        name='invitation-list'),
    # doc ADDING NAME FOR THE URL
    path(
        'invitations/<int:pk>/',
        InvitationDetail.as_view(),
        name='invitation-detail'),
    # doc ADDING NAME FOR THE URL
    path(
        'invitations/<int:pk>/accept/',
        AcceptInvitationView.as_view(),
        name='accept-invitation'),
    # doc ADDING NAME FOR THE URL
]
