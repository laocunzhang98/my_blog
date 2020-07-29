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
