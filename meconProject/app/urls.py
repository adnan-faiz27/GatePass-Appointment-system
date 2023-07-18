from django.urls import path
from . import views


urlpatterns = [
    path('' , views.page , name="page"),
    path('create-guest/' , views.createGuest , name = 'create-guest'),
    path('create-entry/' , views.createEntry , name = 'create-entry'),
    path('create-department/' , views.createDepartment , name = 'create-department'),
    path('create-employee/' , views.createEmployee , name = 'create-employee'),
    path('create-app/' , views.createApp , name = 'create-app'),

    path('view-employee/' , views.viewEmployee , name = 'view-employee'),
    path('employee/<str:pk>/update' , views.updateEmployee , name = 'updateEmployee'),
    path('employee/<str:pk>/delete' , views.deleteEmployee , name = 'deleteEmployee'),

    path('view-app/' , views.viewApp , name = 'view-app'),
    path('app/<str:pk>/update' , views.updateApp , name = 'updateApp'),
    path('app/<str:pk>/delete' , views.deleteApp , name = 'deleteApp'),

    path('view-dep/' , views.viewDep , name = 'view-dep'),
    path('dep/<str:pk>/update' , views.updateDep , name = 'updateDep'),
    path('dep/<str:pk>/delete' , views.deleteDep , name = 'deleteDep'),

    path('view-guest/' , views.viewGuest , name = 'view-guest'),
    path('guest/<str:pk>/update' , views.updateGuest , name = 'updateGuest'),
    path('guest/<str:pk>/delete' , views.deleteGuest , name = 'deleteGuest'),

    path('view-entry/' , views.viewEntry , name = 'view-entry'),
    path('view-entry-checked/<str:pk>/' , views.viewEntryCheck , name = 'viewEntryChecked'),

    path('login/' , views.loginPage , name = 'login'),
    path('register/' , views.registerPage , name = 'register'),
    path('logout/' , views.logoutPage , name = 'logout'),
]