# 基于 Flask + Layui 实现的学生管理系统

#### 介绍

一个简单的基于 Flask + Layui 实现的学生管理系统，分学生端、教师端、管理端三端，主要负责学生管理与学生考试管理。

#### 软件架构

- **后端**：使用 Flask 搭建，SQLAlchemy 作为 ORM 进行数据库操作
- **前端**：采用 Layui 实现简洁 UI
- **数据库**：Mysql
- **用户认证**：使用 Flask-Login 实现登录和会话管理

#### 安装教程

1. **克隆项目到本地**
   
   ```bash
   git clone https://gitee.com/Le2hanG/Students-Management-System.git
   cd Student-Management-System
   ```
   
2. **创建并激活虚拟环境**
   
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **安装依赖项**
   
   ```bash
   pip install -r requirements.txt
   ```

4. **配置数据库**
   确保已安装并启动 MySQL，将项目中的 SQL 文件导入数据库。然后找到项目根目录下的 `config.py` 文件，按照如下格式连接您的数据库：
   
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<host>/<database>'
   ```

5. **启动服务器**
   运行flask run即可成功启动项目

#### 使用说明

1. **用户注册**
   用户可以在系统中注册一个新账号(新账号必须是管理员发布的账号)。填写所需信息后，提交注册表单。
   初始数据库中默认的管理员账号是admin，密码是admin666
2. **用户登录**
   注册成功后，用户可以使用其账号和密码登录系统。输入正确的凭证后，用户将被重定向到主界面。（如果是教师学号进行登录进入的就是教师端，学生学号进行登录进入的就是学生端，在注册前需要联系管理员获取学号，即登录管理员端添加学生或添加教师，在学生表或教师表中有相关信息的人员才能注册登录）
3. **其他功能**
   主要针对管理、教师、学生三端分别设立了不同权限的功能，主要涉及问卷管理与人员信息管理方面。


