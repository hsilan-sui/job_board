from django.urls import path
from .views import index, job_detail,login,signup

urlpatterns = [
    path('', index,name='/'),
    path('job/<int:pk>/', job_detail, name='job-detail'), # name參數會當作html中的連結 ＝>指定位置
    path('login/', login, name="login"),
    path('signup/', signup, name="signup")
]
