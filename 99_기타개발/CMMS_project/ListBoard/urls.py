from django.urls import path
from .views import WorkListListView, WorkListCreate, WorkListDetail, WorkListUpdate, WorkListDelete

urlpatterns = [
    path('', WorkListListView.as_view(), name = 'index'),
    path('create/', WorkListCreate.as_view(), name = 'create'),
    path('<int:pk>/', WorkListDetail.as_view(), name = 'detail'),
    path('<int:pk>/update/', WorkListUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', WorkListDelete.as_view(), name = 'delete'),

]