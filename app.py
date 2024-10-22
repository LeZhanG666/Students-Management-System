from flask import Flask
from models import db
from routes import auth_route, student_route, teacher_route, score_route, exam_route, notice_route, subject_route, home_route
from auth import init_login_manager  # 导入身份验证模块


app = Flask(__name__)

# 加载配置
app.config.from_pyfile('config.py')

# 初始化数据库
db.init_app(app)

# 初始化身份验证
init_login_manager(app)  # 调用函数来初始化 LoginManager

# 注册路由
app.register_blueprint(auth_route.auth)
app.register_blueprint(student_route.student)
app.register_blueprint(teacher_route.teacher)
app.register_blueprint(score_route.score)
app.register_blueprint(exam_route.exam)
app.register_blueprint(notice_route.notice)
app.register_blueprint(subject_route.subject)
app.register_blueprint(home_route.home)

if __name__ == '__main__':
    app.run()
