from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from models import db, Teacher

# 用于存储教师相关的路由
teacher = Blueprint('teacher', __name__)

@teacher.route("/teacher-list-html")
@login_required
def teacher_list_html():
    return render_template('admin/teacher-list.html')

@teacher.route("/add-teacher-html")
@login_required
def add_teacher_html():
    return render_template('admin/add-teacher.html')

# 导入教师接口
@teacher.route('/teachers', methods=['GET'])
@login_required
def get_teachers():
    grade = request.args.get("grade")  # 获取年级筛选条件
    major = request.args.get("major")  # 获取专业筛选条件
    class_name = request.args.get("class_name")  # 获取班级筛选条件
    page = int(request.args.get("page", 1))  # 当前页码，默认为第1页
    per_page = int(request.args.get("per_page", 10))  # 每页显示数量，默认为10

    # 初始化查询对象
    query = Teacher.query

    # 根据筛选条件过滤
    if grade:
        query = query.filter(Teacher.grade == grade)
    if major:
        query = query.filter(Teacher.major == major)
    if class_name:
        query = query.filter(Teacher.class_name == class_name)

    # 计算分页数据
    total = query.count()  # 总记录数
    teachers = query.offset((page - 1) * per_page).limit(per_page).all()  # 分页查询

    # 将教师数据转换为JSON格式
    data = [
        {
            'teacher_id': t.teacher_id,
            'name': t.name,
            'age': t.age,
            'gender': t.gender,
            'grade': t.grade,
            'major': t.major,
            'class_name': t.class_name
        }
        for t in teachers
    ]

    return jsonify({
        'teachers': data,
        'total': total,  # 返回总记录数以计算页数
        'page': page,
        'per_page': per_page
    })

# 删除老师接口
@teacher.route("/delete_teachers", methods=["POST"])
@login_required
def delete_teachers():
    data = request.get_json()  # 获取请求中的 JSON 数据
    ids = data.get('ids', [])  # 提取教师 ID 列表

    if not ids:
        return jsonify(success=False, message="未提供任何教师 ID！"), 400

    # 批量删除教师
    try:
        Teacher.query.filter(Teacher.teacher_id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True, message="删除成功！")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify(success=False, message="删除失败，请重试！", error=str(e)), 500

# 添加教师接口
@teacher.route("/add_teachers", methods=["POST"])
@login_required
def add_teachers():
    name = request.form.get("name")
    teacher_id = request.form.get("teacher_id")
    age = request.form.get("age")
    gender = request.form.get("gender")
    major = request.form.get("major")
    class_name = request.form.get("class_name")
    grade = request.form.get("grade")

    if name and teacher_id and age and gender and major and class_name and grade:
        new_teacher = Teacher(teacher_id=teacher_id, name=name, age=age, gender=gender, major=major, class_name=class_name, grade=grade)
        db.session.add(new_teacher)
        db.session.commit()

        return jsonify(success=True)
    else:
        return jsonify(success=False, message="输入错误")

