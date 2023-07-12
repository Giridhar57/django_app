from django.urls import path
from myapp import views
from myapp.views import NewIssueView

urlpatterns = [
    path('', NewIssueView.as_view(), name='new_issue'),
    path('details/<id>',views.details,name='details'),
    path('allissues',views.all_issues,name='all_issues'),
    path('clear/<id>',views.clear_issue,name='clear_issue'),
    path('delete/<id>',views.delete,name='delete'),
]
