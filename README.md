# Django的建造流程代码
## 建立项目
### 使用venv创建虚拟环境
```python
python3 -m venv ll_env   #使用venv创建一个名为ll_env的虚拟环境
```
### 激活虚拟环境
```python
source ll_env/bin/activate
```
这个命令运行ll_env/bin中的脚本activate。环境处于活动状态时，环境名将包含在圆括号内，在这种情况下，你可以在环境中安装包，并使用已安装的包。在ll_env中安装的包仅在该环境处于活动状态时才可用。

注意 如果你使用的是Windows系统，请使用命令ll_env\Scripts\activate （不包含source ）来激活这个虚拟环境。如果你使用的是PowerShell，可能需要将Activate的首字母大写。

### 停用虚拟环境
```python
deactivate  #要停止使用虚拟环境，可执行命令 deactivate
```

### 安装Django
```python
pip install django
```
别忘了，Django仅在虚拟环境ll_env处于活动状态时才可用。

### 在Django中创建项目
```python
django-admin startproject learning_log .
```
命令让Django新建一个名为learning_log的项目。这个命令末尾的句点让新项目使用合适的目录结构，这样开发完成后可轻松地将应用程序部署到服务器。

注意 千万别忘了这个句点，否则部署应用程序时将遭遇一些配置问题。如果忘记了这个句点，要删除已创建的文件和文件夹（ll_env除外），再重新运行这个命令。

### 创建数据库
```python
python manage.py migrate
```
Django将大部分与项目相关的信息存储在数据库中，因此需要创建一个供Django使用的数据库。

我们将修改数据库称为迁移 （migrate）数据库。首次执行命令migrate 时，将让Django确保数据库与项目的当前状态匹配。在使用SQLite（后面将详细介绍）的新项目中首次执行这个命令时，Django将新建一个数据库。

SQLite是一种使用单个文件的数据库，是编写简单应用程序的理想选择，因为它让你不用太关注数据库管理的问题。

注意 在虚拟环境中运行manage.py时，务必使用命令python，即便你在运行其他程序时使用的是另外的命令，如python3。在虚拟环境中，命令python 指的是在虚拟环境中安装的Python版本。

### 查看项目
```python
python manage.py runserver
```
Django启动了一个名为development server的服务器，让你能够查看系统中的项目，了解其工作情况。如果你在浏览器中输入URL以请求页面，该Django服务器将进行响应：生成合适的页面，并将其发
送给浏览器。

## 创建应用程序
当前，在前面打开的终端窗口中应该还运行着runserver 。请再打开一个终端窗口（或标签页），并切换到manage.py所在的目录。激活虚拟环境，再执行命令startapp
```python
source ll_env/bin/activate
python manage.py startapp learning_logs
```
命令startapp appname 让Django搭建创建应用程序所需的基础设施。如果现在查看项目目录，将看到其中新增了文件夹learning_logs

### 定义模型
我们来想想涉及的数据。每位用户都需要在学习笔记中创建很多主题。用户输入的每个条目都与特定主题相关联，这些条目将以文本的方式显示。我们还需要存储每个条目的时间戳，以便告诉用户各个条目都是什么时候创建的。

打开文件`models.py`，看看它当前包含哪些内容
```python
from django.db import models
# 在这里创建模型。
```
这里导入了模块models ，并让我们创建自己的模型。模型告诉Django如何处理应用程序中存储的数据。在代码层面，模型就是一个类，就像前面讨论的每个类一样，包含属性和方法。下面是表示用户将存储的主题的模型
```python
from django.db import models
class Topic(models.Model):
"""用户学习的主题。"""
 text = models.CharField(max_length=200)
 date_added = models.DateTimeField(auto_now_add=True)
 def __str__(self):
"""返回模型的字符串表示。"""
return self.text
```
我们创建了一个名为Topic 的类，它继承Model ，即Django中定义了模型基本功能的类。我们给Topic 类添加了两个属性：text 和date_added 。

属性text 是一个CharField ——由字符组成的数据，即文本。需要存储少量文本，如名称、标题或城市时，可使用CharField 。定义CharField 属性时，必须告诉Django该在数据库中预留多少空间。这里将max_length 设置成了200（即200字符），这对存储大多数主题名来说足够了。

属性date_added 是一个DateTimeField ——记录日期和时间的数据。我们传递了实参auto_now_add=True ，每当用户创建新主题时，Django都会将这个属性自动设置为当前日期和时间。

需要告诉Django，默认使用哪个属性来显示有关主题的信息。Django调用方法__str__() 来显示模型的简单表示。这里编写了方法__str__() ，它返回存储在属性text 中的字符串

### 激活模型
要使用这些模型，必须让Django将前述应用程序包含到项目中。为此，打开`settings.py`（它位于目录`learning_log/learning_log`中），其中有个片段告诉Django哪些应用程序被安装到了项目中并将协同工作。
```python
--snip--
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
]
--snip--
```
请将INSTALLED_APPS 修改成下面这样，将前面的应用程序添加到这个列表中

```python
--snip--
INSTALLED_APPS = [
# 我的应用程序
'learning_logs',
# 默认添加的应用程序
'django.contrib.admin',
--snip--
]
--snip--
```
通过将应用程序编组，在项目不断增大，包含更多的应用程序时，有助于对应用程序进行跟踪。这里新建了一个名为“我的应用程序”的片段，当前它只包含应用程序learning_logs 。务必将自己创建的应用程序放在默认应用程序前面，这样能够覆盖默认应用程序的行为。

接下来，需要让Django修改数据库，使其能够存储与模型Topic 相关的信息。为此，在终端窗口中执行下面的命令
```python
python manage.py makemigrations learning_logs
```
命令makemigrations 让Django确定该如何修改数据库，使其能够存储与前面定义的新模型相关联的数据。输出表明Django创建了一个名为0001_initial.py的迁移文件，这个文件将在数据库中为模型
Topic 创建一个表。

下面应用这种迁移，让Django替我们修改数据库
```python
python manage.py migrate
```
```python
Operations to perform:
Apply all migrations: admin, auth, contenttypes, learning_logs, sessions
Running migrations:
❶ Applying learning_logs.0001_initial... OK
```
这个命令的大部分输出与首次执行命令migrate 的输出相同。需要检查的是❶输出行。在这里，Django指出为learning_logs应用迁移时一切正常。

每当需要修改项目管理的数据时，都采取如下三个步骤：修改`models.py`，对learning_logs 调用`makemigrations` ，以及让Django迁移项目。

### Django管理网站
Django提供的管理网站 （admin site）让你能够轻松地处理模型。网站管理员可以使用管理网站，但普通用户不能使用。本节将建立管理网站，并通过它使用模型Topic 来添加一些主题。
#### 创建超级用户
Django允许创建具备所有权限的用户，即超级用户 。权限 决定了用户可执行的操作。最严格的权限设置只允许用户阅读网站的公开信息。注册用户通常可阅读自己的私有数据，还可查看一些只有会员才能查看的信息。为有效地管理Web应用程序，网站所有者通常需要访问网站存储的所有信息。优秀的管理员会小心对待用户的敏感信息，因为用户极其信任自己访问的应用程序。

为在Django中创建超级用户，请执行下面的命令并按提示做

```python
python manage.py createsuperuser
```
输出：
```python
❶ Username (leave blank to use 'eric'): ll_admin
❷ Email address:
❸ Password:
Password (again):
Superuser created successfully.
```
你执行命令createsuperuser 时，Django提示输入超级用户的用户名（见❶）。这里输入的是ll_admin，但可输入任何用户名。如果你愿意，可以输入电子邮箱地址，也可让这个字段为空（见❷）。需要输入密码两次（见❸）。

注意 一些敏感信息可能会向网站管理员隐藏。例如，Django并不存储你输入的密码，而是存储从该密码派生出来的一个字符串，称为散列值 。每当你输入密码时，Django都计算其散列值，并将结果与存储的散列值进行比较。如果这两个散列值相同，你就通过了身份验证。由于存储的是散列值，即便黑客获得了网站数据库的访问权，也只能获取其中存储的散列值，无法获得密码。在网站配置正确的情况下，几乎无法根据散列值推导出原始密码。

#### 向管理网站注册模型
Django自动在管理网站中添加了一些模型，如User 和Group，但对于我们创建的模型，必须手工进行注册。

我们创建应用程序learning_logs 时，Django在`models.py`所在的目录中创建了一个名为`admin.py`的文件
```python
from django.contrib import admin
# 在这里注册你的模型。
```
为向管理网站注册Topic ，请输入下面的代码
```python
from django.contrib import admin
❶ from .models import Topic
❷ admin.site.register(Topic)
```
这些代码首先导入要注册的模型Topic （见❶）。models 前面的句点让Django在`admin.py`所在的目录中查找`models.py`。`admin.site.register()` 让Django通过管理网站管理模型（见❷）。

现在，使用超级用户账户访问管理网站：访问`http://localhost:8000/admin/`，并输入刚创建的超级用户的用户名和密码。

注意 如果在浏览器中看到一条消息，指出访问的网页不可用，请确认在终端窗口中运行着Django服务器。如果没有，请激活虚拟环境，并执行命令`python manage.py runserver` 。在开发过程中，如果无法通过浏览器访问项目，首先应采取的故障排除措施是，关闭所有打开的终端，再打开终端并执行命令`runserver` 。

#### 添加主题
向管理网站注册Topic 后，我们来添加第一个主题。为此，单击Topics进入主题页面，它几乎是空的，因为还没有添加任何主题。单击Add，将出现一个用于添加新主题的表单。在第一个方框中输入Chess ，再单击Save回到主题管理页面，其中包含刚创建的主题。

下面再创建一个主题，以便有更多的数据可供使用。再次单击Add，并输入Rock Climbing，然后单击Save回到主题管理页面。现在，你可以看到其中包含了主题Chess和RockClimbing 。

注释：主题其实就是标题，此处指栏目标题

### 定义模型
要记录学到的国际象棋和攀岩知识，用户必须能够在学习笔记中添加条目。为此，需要定义相关的模型。每个条目都与特定主题相关联，这种关系称为多对一关系 ，即多个条目可关联到同一个主题。

下面是模型Entry 的代码，请将这些代码放在文件`models.py`中
```python
from django.db import models
class Topic(models.Model):
--snip--
❶ class Entry(models.Model):
"""学到的有关某个主题的具体知识。"""
❷ topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
❸ text = models.TextField()
date_added = models.DateTimeField(auto_now_add=True)
❹ class Meta:
verbose_name_plural = 'entries'
def __str__(self):
""""""返回模型的字符串表示。"""
❺ return f"{self.text[:50]}..."
```
像Topic 一样，Entry 也继承了Django基类Model （见❶）。第一个属性topic 是个ForeignKey 实例（见❷）。外键 （foreignkey）是一个数据库术语，它指向数据库中的另一条记录，这里是将每个条目关联到特定主题。创建每个主题时，都分配了一个键（ID）。需要在两项数据之间建立联系时，Django使用与每项信息相关联的键。

我们稍后将根据这些联系获取与特定主题相关联的所有条目。实参`on_delete=models.CASCADE` 让Django在删除主题的同时删除所有与之相关联的条目，这称为级联删除 （cascading delete）。

接下来是属性text ，它是一个TextField 实例（见❸）。这种字段的长度不受限制，因为我们不想限制条目的长度。属性`date_added` 让我们能够按创建顺序呈现条目，并在每个条目旁边放置时间戳。

在❹处，我们在Entry 类中嵌套了Meta 类。Meta 存储用于管理模型的额外信息。在这里，它让我们能够设置一个特殊属性，让Django在需要时使用Entries 来表示多个条目。如果没有这个类，Django将使用Entrys 来表示多个条目。

方法`__str__()` 告诉Django，呈现条目时应显示哪些信息。条目包含的文本可能很长，因此让Django只显示text 的前50字符（见❺）。我们还添加了一个省略号，指出显示的并非整个条目。

### 迁移模型Entry
添加新模型后，需要再次迁移数据库。你将慢慢地对这个过程了如指掌：修改`models.py`，执行命令`python manage.py makemigrations app_name` ，再执行命令`python manage.py migrate` 。

app_name是指应用程序的名字

### 向管理网站注册Entry
我们还需要注册模型Entry 。为此，需要将admin.py修改成类似于下面这样
```python
from django.contrib import admin
from .models import Topic, Entry
admin.site.register(Topic)
admin.site.register(Entry)
```
返回到http://localhost/admin/，你将看到Learning_Logs下列出了Entries。单击Entries的Add链接，或者单击Entries再选择Add entry，将看到一个下拉列表，供你选择要为哪个主题创建条目，以
及一个用于输入条目的文本框。

## 创建页面
### 映射URL
用户通过在浏览器中输入URL以及单击链接来请求页面，因此我们要确定项目需要哪些URL。主页的URL最重要，它是用户用来访问项目的基础URL。当前，基础URL（`http://localhost: 8000/`）返回默认的Django网站，让我们知道正确地建立了项目。下面修改这一点，将这个基础URL映射到“学习笔记”的主页。

打开项目主文件夹learning_log中的文件urls.py，你将看到如下代码

```python
❶ from django.contrib import admin
from django.urls import path
❷ urlpatterns = [
❸ path('admin/', admin.site.urls),
]
```
前两行导入了一个模块和一个函数，以便对管理网站的URL进行管理（见❶）。这个文件的主体定义了变量`urlpatterns` （见❷）。在这个针对整个项目的`urls.py`文件中，变量`urlpatterns` 包含项目中应用程序的URL。❸处的代码包含模块`admin.site.urls` ，该模块定义了可在管理网站中请求的所有URL。

我们需要包含learning_logs 的URL，因此添加如下代码
```python
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
path('admin/', admin.site.urls),
❶ path('', include('learning_logs.urls')),
]
```
在❶处，添加一行代码来包含模块`learning_logs.urls` 。

默认的`urls.py`包含在文件夹learning_log中，现在需要在文件夹learning_logs中再创建一个`urls.py`文件。为此，新建一个文件，使用文件名`urls.py`将其存储到文件夹`learning_logs`中，再在这个文件中输入如下代码
```python
❶ """定义learning_logs的URL模式。"""
❷ from django.urls import path
❸ from . import views
❹ app_name = 'learning_logs'
❺ urlpatterns = [
# 主页
❻ path('', views.index, name='index'),
]
```
为指出当前位于哪个`urls.py`文件中，在该文件开头添加一个文档字符串（见❶）。接下来，导入了函数`path` ，因为需要使用它将URL映射到视图（见❷）。我们还导入了模块`views` （见❸），其中的句点让Python从当前`urls.py`模块所在的文件夹导入`views.py`。变量`app_name` 让Django能够将这个`urls.py`文件同项目内其他应用程序中的同名文件区分开来（见❹）。在这个模块中，变量`urlpatterns` 是一个列表，包含可在应用程序`learning_logs` 中请求的页面。

实际的URL模式是对函数`path() `的调用，这个函数接受三个实参（见❺）。第一个是一个字符串，帮助Django正确地路由（route）请求。收到请求的URL后，Django力图将请求路由给一个视图。为此，它搜索所有的URL模式，找到与当前请求匹配的那个。

Django忽略项目的基础URL（`http://localhost:8000/`），因此空字符串（''）与基础URL匹配。其他URL都与这个模式不匹配。如果请求的URL与任何既有的URL模式都不匹配，Django将返回一个错误页
面。

`path() `的第二个实参（见❻）指定了要调用`view.py`中的哪个函数。请求的URL与前述正则表达式匹配时，Django将调用`view.py`中的函数`index()` （这个视图函数将在下一节编写）。第三个实参将这个URL模式的名称指定为`index` ，让我们能够在代码的其他地方引用它。每当需要提供到这个主页的链接时，都将使用这个名称，而不编写URL。

### 编写识图
视图函数接受请求中的信息，准备好生成页面所需的数据，再将这些数据发送给浏览器——这通常是使用定义页面外观的模板实现的。

`learning_logs`中的文件`views.py`是执行命令`python manage.py startapp` 时自动生成的，当前其内容如下
```python
from django.shortcuts import render
# 在这里创建视图。
```
当前，这个文件只导入了函数render() ，它根据视图提供的数据渲染响应。请在这个文件中添加为主页编写视图的代码，如下所示
```python
from django.shortcuts import render
def index(request):
"""学习笔记的主页。"""
    return render(request, 'learning_logs/index.html')
```
URL请求与刚才定义的模式匹配时，Django将在文件`views.py`中查找函数`index() `，再将对象`request` 传递给这个视图函数。这里不需要处理任何数据，因此这个函数只包含调用`render()` 的代码。这里向函数`render()` 提供了两个实参：对象`request` 以及一个可用于创建页面的模板。下面来编写这个模板。

## 创建其他页面
### 模板继承
创建网站时，一些通用元素几乎会在所有页面中出现。在这种情况下，可编写一个包含通用元素的父模板，并让每个页面都继承这个模板，而不必在每个页面中重复定义这些通用元素。这种方法能让
你专注于开发每个页面的独特方面，还能让修改项目的整体外观容易得多。
#### 父模板
下面创建一个名为base.html的模板，并将其存储在index.html所在的目录中。这个模板包含所有页面都有的元素，而其他模板都继承它。当前，所有页面都包含的元素只有顶端的标题。因为每个页面都包含这个模板，所以将这个标题设置为到主页的链接
```html
<p>
❶ <a href="{% url 'learning_logs:index' %}">Learning Log</a>
</p>
❷ {% block content %}{% endblock content %}
```
这个文件的第一部分创建一个包含项目名的段落，该段落也是到主页的链接。为创建链接，使用了一个模板标签 ，它是用花括号和百分号（{% %} ）表示的。

模板标签是一小段代码，生成要在页面中显示的信息。这里的模板标签{% url
'learning_logs:index' %} 生成一个URL，该URL与在learning_logs/urls.py中定义的名为'index' 的URL模式匹配（见❶）。在本例中，learning_logs 是一个命名空间 ，而index 是该命名空间中一个名称独特的URL模式。这个命名空间来自在文件learning_logs/urls.py中赋给app_name 的值。

通过使用模板标签来生成URL，能很容易地确保链接是最新的：只需修改urls.py中的URL模式，Django就会在页面下次被请求时自动插入修改后的URL。在本项目中，每个页面都将继承base.html，因此从现在开始，每个页面都包含到主页的链接。

在❷处，我们插入了一对块 标签。这个块名为content ，是一个占位符，其中包含的信息由子模板指定。子模板并非必须定义父模板中的每个块，因此在父模板中，可使用任意多个块来预留空间，而子模板可根据需要定义相应数量的块。

#### 子模板
现在需要重写index.html，使其继承base.html。为此，向index.html添加如下代码
```html
❶ {% extends "learning_logs/base.html" %}
❷ {% block content %}
<p>Learning Log helps you keep track of your learning, for any topic you're
learning about.</p>
❸ {% endblock content %}
```
如果将这些代码与原来的index.html进行比较，将发现标题Learning Log没有了，取而代之的是指定要继承哪个模板的代码（见❶）。子模板的第一行必须包含标签{% extends %}，让Django知道它继承了哪个父模板。文件base.html位于文件夹learning_logs中，因此父模板路径中包含learning_logs。这行代码导入模板base.html的所有内容，让index.html能够指定要在content 块预留的空间中添加的内容。

在❷处，插入了一个名为content 的{% block %} 标签，以定义content 块。不是从父模板继承的内容都包含在content块中，在这里是一个描述项目“学习笔记”的段落。在❸处，使用标签{% endblock content %} 指出了内容定义的结束位置。在标签{% endblock %} 中，并非必须指定块名，但如果模板包含多个块，指定块名有助于确定结束的是哪个块。

模板继承的优点开始显现出来了：在子模板中，只需包含当前页面特有的内容。这不仅简化了每个模板，还使得网站修改起来容易得多。要修改很多页面都包含的元素，只需修改父模板即可，所做的修改将传导到继承该父模板的每个页面。在包含数十乃至数百个页面的项目中，这种结构使得网站改进起来更容易、更快捷。

注意 在大型项目中，通常有一个用于整个网站的父模板base.html，且网站的每个主要部分都有一个父模板。每个部分的父模板都继承base.html，而网站的每个页面都继承相应部分的父模板。这让你能够轻松地修改整个网站的外观、网站任何一部分的外观以及任何一个页面的外观。这种配置提供了一种效率极高的工作方式，让你乐意不断地去改进网站。