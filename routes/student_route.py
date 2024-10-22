# 用处储存学生有关的路由

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Student, Teacher, User

student = Blueprint('student', __name__)

@student.route("/student-list-html")
@login_required
def student_list_html():
    if current_user.role=="admin":
        return render_template('admin/student-list.html')
    if current_user.role=="teacher":
        return render_template('teacher/student-list.html')

@student.route("/add-student-html")
@login_required
def add_student_html():
    if current_user.role=="admin":
        return render_template('admin/add-student.html')
    if current_user.role=="teacher":
        return render_template('teacher/add-student.html')

# 导入学生接口
@student.route('/students', methods=['GET'])
@login_required
def get_students():
    grade = request.args.get("grade")
    major = request.args.get("major")
    class_name = request.args.get("class_name")
    page = int(request.args.get("page", 1))  # 当前页码，默认为第1页
    per_page = int(request.args.get("per_page", 10))  # 每页显示数量，默认为10

    # 初始化查询对象
    query = Student.query

    # 根据筛选条件过滤
    if grade:
        query = query.filter(Student.grade == grade)
    if major:
        query = query.filter(Student.major == major)
    if class_name:
        query = query.filter(Student.class_name == class_name)

    if current_user.role == "teacher":
        current_teacher = Teacher.query.join(User, User.username==Teacher.teacher_id).filter(User.username==current_user.username).first()
        query = query.filter(Student.grade == current_teacher.grade, Student.major == current_teacher.major, Student.class_name == current_teacher.class_name)

    # 计算分页数据
    total = query.count()  # 总记录数
    students = query.offset((page - 1) * per_page).limit(per_page).all()  # 分页查询

    # 将学生数据转换为JSON格式
    data = [
        {
            'student_id': s.student_id,
            'name': s.name,
            'age': s.age,
            'gender': s.gender,
            'grade': s.grade,
            'major': s.major,
            'class_name': s.class_name
        }
        for s in students
    ]

    return jsonify({
        'students': data,
        'total': total,  # 返回总记录数以计算页数
        'page': page,
        'per_page': per_page
    })

# 删除学生接口
@student.route("/delete_students", methods=["POST"])
@login_required
def delete_students():
    data = request.get_json()  # 获取请求中的 JSON 数据
    ids = data.get('ids', [])  # 提取学生 ID 列表

    if not ids:
        return jsonify(success=False, message="未提供任何学生 ID！"), 400

    # 批量删除学生
    try:
        Student.query.filter(Student.student_id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True, message="删除成功！")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify(success=False, message="删除失败，请重试！", error=str(e)), 500

# 添加学生接口
@student.route("/add_students", methods=["POST"])
@login_required
def add_student():
    name = request.form.get("name")
    student_id = request.form.get("student_id")
    age = request.form.get("age")
    grade = request.form.get("grade")
    class_name = request.form.get("class")
    gender = request.form.get("gender")
    major = request.form.get("major")

    if current_user.role == "teacher":
        if name and student_id and age and gender:
            current_teacher = Teacher.query.join(User, User.username==Teacher.teacher_id).filter(User.username==current_user.username).first()
            new_student = Student(student_id=student_id, name=name, age=age, gender=gender, grade=current_teacher.grade, major=current_teacher.major, class_name=current_teacher.class_name)    
    else:
        if name and student_id and age and gender and grade and class_name and major:
            new_student = Student(student_id=student_id, name=name, age=age, gender=gender, grade=grade, major=major, class_name=class_name)
    
    if new_student:
        db.session.add(new_student)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="错误")

# 获取学生姓名
@student.route('/student_name/<student_id>', methods=['GET'])
@login_required
def get_student_name(student_id):
    # 根据学生 ID 查询学生信息
    student = Student.query.filter(Student.student_id == student_id).first()
    
    if student:
        return jsonify({'name': student.name})  # 返回学生姓名
    else:
        return jsonify({'error': '学生未找到'}), 404  # 返回404错误
