# job_board django 專案

## Django 初始化儀式

1. 創建虛擬環境

```bash
python3 -m venv env # 虛擬環境名字為env
```

2.執行之後=>虛擬環境 env 已經創建 3.啟動虛擬環境

- MAC /LINUX

```bash
source env/bin/activate
```

4. 安裝 Django

```bash
pip3 install django
```

5.創建一個新的 Django Project

```bash
django-admin startproject config .
```

6. 創建第一個 app

```bash
python3 manage.py startapp job_board
```

7. 到 config/settings.py 增加 job_board 至 INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'job_board', # 加上剛剛創建的第一個movies app
]

```

8. 在 job_board/創建檔案 urls.py

- 就是把 job_board 中的 url 集中起來 到時候一次引入在 config/urls.py

```python
# 在job_board/urls.py
from django.urls import path

urlpatterns = [
    path('', index),
]

```

9. 回到 config/urls.py

- 導入 include 這個方法

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job_board.urls')) #把job_board中的urls檔引入進來
]

```

10. 現在就可以專門針對 job_board 的 app 進行開發 -到 job_board/views 新增 index 函式

```python
from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('<h1>開始找工作啦！</h1>')
```

11. 回到 job_board/urls.py

- 記得引入 views

```python
from django.urls import path
from .views import index #這行

urlpatterns = [
    path('', index),
]
```

## 創建 model

- 當我們創建 django 專案 預設就是使用`db.sqlite3`資料庫(嵌入式資料庫)

  - 若使用 MySQL or PostgreSQL NoSQL 會在伺服器上運行
  - 不過 django 很容易與不同資料庫 隨插即用

- model 就是 python 的 class
- model 也代表 database 中的一個 table 表
- 在 class 中的 attributes 代表就是 table 中的一個欄位

- 在 job_board/models.py 預設就有這個檔案

```python
from django.db import models
```

### 首先要先定義 model 這個『資料表』的 schema

- 創建 job_posting 資料表=> 思考一下 table schema
  - title, description, company, salary
  - 在 django 中的 model 要定義 schema 的 資料型別可以參考 [Field types](https://docs.djangoproject.com/en/5.0/ref/models/fields/#field-types)

```python
from django.db import models

# Create your models here.
class JobPosting(models.Model): # 讓class JobPosting 這個類繼承models.Model
    # id - starts at 1 and autoincrements
    title = models.CharField(max_length=100) # mysql varchar(100)
    description = models.TextField() # mysql text
    company = models.CharField(max_length=100)
    salary = models.IntegerField() # mysql int
```

## 讓 django 知道要在該資料庫 db.sqlite3 創建這個 model 資料表

- 兩個指令

```python
# makemigration => 創建指令，告訴django database的改變 => 可以說是條列出資料庫的更改內容
python3 manage.py makemigrations
# migrate => 正是下這個指令就是說 將剛剛資料庫變化的狀態 正是寫入到資料庫/正式生效
python3 manage.py migrate
```

## 模型管理器（Model Manager） => 預設是 objects 管理器

- 創建的`class JobPosting(models.Model): # 讓class JobPosting 這個類繼承models.Model`=> 模型管理器（Model Manager）
- 在 Django 中，每個模型（Model）都可以有一個或多個模型管理器 Model Manager
  - 模型管理器是一個 Python 對象 objects，它封裝了對數據庫的查詢操作，允許您在模型層面上進行數據庫操作，如查詢、創建、更新和刪除對象
- Django 為每個模型 model 添加了一個名為 objects 的管理器。這是因為 Django 提供了 `django.db.models.Manager`類的默認實例，並將其賦值給 objects 屬性

```python
JobPosting.object.all() # 可以得到JobPosting資料表的所有物件
JobPosting.object.get(id=1)
JobPosting.object.filter(title='job title')
```

### Django 提供了 shell ＝> 可以直接從 terminal 與資料庫的資料表進行操作

- 要使用 shell，首先要先啟用虛擬環境

```bash
source env/bin/activate
```

- 使用 Django 提供的 shell (離開 shell 按 exit() / ctrl+Z)

```bash
python3 manage.py shell
```

- 引入 JobPosting 這個 model（資料表 ／類）＝> 就可以使用 JobPosting 的模型管理器來操作該資料表的 CRUD

  > 從`job_board/目錄中的models.py檔案來引入其中的JobPosting model(資料表 ／類）`

- crud 操作：

```bash
from job_board.models import JobPosting
JobPosting.objects.all()  # <QuerySet []>

JobPosting.objects.create(title="full stack developer", description="manage web using python with django and ai tool", company="tribool", salary=72000) # <JobPosting: JobPosting object (1)>

JobPosting.objects.all()
# <QuerySet [<JobPosting: JobPosting object (1)>]>

job = JobPosting.objects.get(id=1)
job #  <JobPosting: JobPosting object (1)>

job.description
# 'manage web using python with django and ai tool'

job.description = 'just python hooray!!!'
job.description
# 'just python hooray!!!'

job.save()
#  save() 方法是用於將新創建的對象或者已修改的對象保存到數據庫中的方法

job.delete()
# (1, {'job_board.JobPosting': 1})

JobPosting.objects.all()
# <QuerySet []> 資料已被刪除

# 獲取所有的 JobPosting 對象並刪除它們(直接操作數據庫)
JobPosting.objects.all().delete()
```

### 增加欄位到 JobPosting 的 model/資料表/類

- 每次更動同一個 model 欄位
- 肌肉記憶就要自動=>
- `=> python3 manage.py makegrations`
- `=> python3 manage.py migrate`

## 如何把資料表的資料 顯示在 template/網頁上 =>view

- 跟 model 資料溝通交換

  - ＝> 主要是 view
  - => view 在把資料傳遞到 template 顯現在網頁上

- 首先 在 Job_board app/views

```python
from django.shortcuts import render,HttpResponse

from .models import JobPosting # 引入model

# Create your views here.
def index(request):
    # 這裡可以像在django shell一樣使用models manager來跟資料庫互動
    jobs = JobPosting.objects.all()
    print(jobs)
    return HttpResponse('<h1>開始找工作啦！</h1>')
```

- `python3 manage.py runserver`

  - 啟動伺服器會看到終端機 print 出 Queryset

- 上面這段是表示 views 和 models 進行交流

- 接下來要示範 views 從 model 那裡拿到資料表的 data 後，要怎麼顯示在 template 上?

```python
def index(request):
    # 這裡可以像在django shell一樣使用models manager來跟資料庫互動
    # 我只想要欄位is_active=True的資料
    active_postings = JobPosting.objects.filter(is_active=True)
    # 需要把data資料組織起來作為參數 傳遞render() 給templates
    context = {
      'job_postings': active_postings
    }
    print(jobs)
    return renter(request, 'job_board/index.html' context)
```

## views 做好了工作，但還需要建置屬於 job_board／app 的 Templates

- 在 job_board／建立 templates 資料夾
  - 所以在 job_board/templates/建立`_base.html` 將作為網站的骨架
  - 接著 job_board/templates/job_board/建立 index.html
    - 這個 index.html 將繼承`extends _base.html`

## 404 處理

- 在 views 引入套件 `get_object_or_404`

```python=

```

## 認識 Django-admin

- 網址輸入`http://127.0.0.1:8000/admin`
- Django admin 是與 model 和 資料庫 進行圖形交互的好方法
- 停止 server

- 創建一個管理員『超級使用者』(擁有所有許可權的使用者，可以做任何他們想做的事)

```bash=
python3 manager.py createsuperuser
```

- 設置帳戶名 email 與密碼
- 重新`python3 manage.py runserver`
- 登入 admin 帳戶密碼＝>即可成功登入後台

## 向 Django-admin 註冊 job_board app 的 models(資料表)

- 到 job_board/ 下的`admin.py`

```python
from django.contrib import admin  # 預設就有的
```

- 首先先導入 job_board/models.py 中的模型/資料表 JobPosting
  - 接著跟 admin 註冊 JobPosting 該模型/資料表

```python
from django.contrib import admin
from  .models import JobPosting

admin.site.register(JobPosting)
```

- `admin.site.register()` 是 Django 中用來將模型註冊到後台管理界面的函數。通過這個函數，你可以告訴 Django 管理員界面需要管理哪些模型（即資料庫表）以及如何展示它們

- 重新`$python3 manage.py runserver`=> 到 django 中的管理員 admin/

  - 會看到 admin 中的 dashboard 會出現 job_board 這個 model/資料表
  - 會將 JobPosting 的資料變成=>`JobPosting object (1)`呈現出來

- 但若想要再登入後台時清楚看到該模型/資料表的語意內容
  - 就可以在該 models 檔案來做一些客製化
  - 我想在 admin 中的 dashboard 呈現該 model 時想要呈現招聘職缺 ｜ 服務的公司 ｜ 活動狀態

```python
# 在models/下的JobPosting 覆寫__str__
from django.db import models

# Create your models here.
class JobPosting(models.Model):
    # id - starts at 1 and autoincrements
    title = models.CharField(max_length=100) # mysql varchar(100)
    description = models.TextField() # mysql text
    company = models.CharField(max_length=100)
    salary = models.IntegerField() # mysql int
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} | {self.company} | Active: {self.is_active}"
```
