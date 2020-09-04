### 确认你的电脑已经正确安装 Python 3.4 以上的版本。

### 下载项目后，在命令行中进入项目目录，并创建虚拟环境：

python -m venv env
### 运行虚拟环境（Windows环境）:

env\Scripts\activate.bat
### 或（Linux环境）：

source env/bin/activate
### 自动安装所有依赖项：

pip install -r requirements.txt
### 然后进行数据迁移：

python manage.py migrate
### 最后运行测试服务器：

python manage.py runserver
### 项目就运行起来了。
### 项目实现主要功能
 - 发表新文章

- 删除文章

- 修改文章

- 用户的登录和登出

- 用户的注册

- 用户的删除

- 重置用户密码

- 扩展用户信息

- 上传用户头像

- 文章分页

- 文章浏览量

- 最热文章

- 文章栏目

- 文章标签

- 富文本编辑器

- 文章标题图

- 发表评论

- 留言
