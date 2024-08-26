from django.shortcuts import render,HttpResponse, get_object_or_404

from .models import JobPosting # 引入model

# Create your views here.
def index(request):
    # 這裡可以像在django shell一樣使用models manager來跟資料庫互動
    # 我只想要欄位is_active=True的資料
    active_postings = JobPosting.objects.filter(is_active=True)
    # 需要把data資料組織起來作為參數 傳遞render() 給templates
    context = {
      'job_postings': active_postings,
    }

    return render(request, 'job_board/index.html', context)

def job_detail(request, pk):
    #job_posting = JobPosting.objects.get(pk=pk) # .get()取得pk=1的單筆資料
    job_posting = get_object_or_404(JobPosting, pk=pk, is_active=True) # 使用get_object_or_404() # debug=True
    context = {
      'posting': job_posting  
    } 
    return render(request,'job_board/detail.html',context)

def login(request):
    return render(request,'job_board/login.html')


def signup(request):
    return render(request,'job_board/signup.html')