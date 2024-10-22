# 用于储存登录注册登出有关的路由

from flask import Blueprint, request, jsonify, render_template
from models import db, User, Student, Teacher
from flask_login import login_user, logout_user, login_required, current_user

# 登录路由
auth = Blueprint('auth', __name__)

# 重定向
@auth.route('/', methods=["GET"])
def home():
    return render_template('login.html')

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha = request.form.get("captcha")

        if not username or len(username) < 3:
            return jsonify(success=False, message="用户名至少为3个字符！")
            
        if not password or len(password) < 6:
            return jsonify(success=False, message="密码至少为6个字符！")


        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return jsonify(success=True,role = user.role)
        else:
            return jsonify(success=False, message="用户名或密码错误！")

    return render_template('login.html')
    
@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': '成功退出'}), 200  # 返回成功消息和状态码

# 注册路由
# 注册路由
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or len(username) < 3:
            return jsonify(success=False, message="用户名至少为3个字符！")
            
        if not password or len(password) < 6:
            return jsonify(success=False, message="密码至少为6个字符！")
            
        if not confirm_password or password != confirm_password:
            return jsonify(success=False, message="两次密码输入不一致！")

        # 检查用户名是否在 students 或 teachers 表中
        student = Student.query.filter_by(student_id=username).first()
        teacher = Teacher.query.filter_by(teacher_id=username).first()

        if not student and not teacher:
            return jsonify(success=False, message="该用户名不存在，请联系管理员获取账号！")

        # 根据用户名的来源决定角色
        role = "student" if student else "teacher"

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify(success=False, message="用户名已存在，请选择其他用户名！")

        # 创建新用户
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(success=True)

    return render_template('register.html')

@auth.route("/get_info", methods=["GET"])
def get_info():
    id = current_user.username
    pwd = current_user.password
    
    if current_user.role == 'student':
        current_student = Student.query.join(User, User.username==Student.student_id).filter(User.username==current_user.username).first()
        major = current_student.major
        class_name = current_student.class_name
        grade = current_student.grade
        name = Student.query.filter_by(student_id=id).first().name
        role = "学生"

    if current_user.role == 'teacher':
        current_teacher = Teacher.query.join(User, User.username==Teacher.teacher_id).filter(User.username==current_user.username).first()
        major = current_teacher.major
        class_name = current_teacher.class_name
        grade = current_teacher.grade
        name = Teacher.query.filter_by(teacher_id=id).first().name
        role = "教师"

    if current_user.role == 'admin':
        major = ""
        class_name = ""
        grade = ""
        name = "管理员"
        role = "管理员"
    
    return jsonify({
        "id": id,
        "pwd": pwd,
        "name": name,
        "role": role,
        "major": major,
        "class_name": class_name,
        "grade": grade
    })

@auth.route("/update_info", methods=["POST"])
def update_info():
    data = request.get_json()
    id = current_user.username

    # 根据角色更新用户信息
    if current_user.role == 'student':
        student = Student.query.filter_by(student_id=id).first()
        if student:
            student.name = data.get('name', student.name)  # 更新姓名
            current_user.password = data.get('pwd', current_user.password) # 更新密码(暂未规定长度)
            db.session.commit()
            return jsonify({"message": "信息更新成功！"})
        else:
            return jsonify({"message": "未找到用户！"}), 404
            
    elif current_user.role == 'admin':
            current_user.password = data.get('pwd', current_user.password) # 更新密码(暂未规定长度)
            db.session.commit()
            return jsonify({"message": "信息更新成功！"})

    return jsonify({"message": "无效的用户角色！"}), 400