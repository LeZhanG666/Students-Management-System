# 用于存放三端的主页需要用到的api
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import Teacher, Student, Subject, Exam, Score, User
from auth import role_required

home = Blueprint('home', __name__)

@home.route('/admin-html')
@login_required
@role_required('admin')
def admin_html():
    return render_template('admin/admin.html')

@home.route('/student-html')
@login_required
@role_required('student')
def student_html():
    return render_template('student/student.html')

@home.route('/teacher-html')
@login_required
@role_required('teacher')
def teacher_html():
    return render_template('teacher/teacher.html')

@home.route('/admin-home-html')
@login_required
def admin_home_html():
    return render_template('admin/admin-home.html')

@home.route('/student-home-html')
@login_required
def student_home_html():
    return render_template('student/student-home.html')

@home.route('/teacher-home-html')
@login_required
def teacher_home_html():
    return render_template('teacher/teacher-home.html')

@home.route('/get_count', methods=['GET'])
def get_dashboard_data():
    teacher_count = Teacher.query.count()
    student_count = Student.query.count()
    subject_count = Subject.query.count()
    exam_count = Exam.query.count()
    if current_user.role == "student":
        current_student = Student.query.join(User, User.username==Student.student_id).filter(User.username==current_user.username).first()
        student_class_count = Student.query.filter(Student.class_name==current_student.class_name, Student.major==current_student.major, Student.grade==current_student.grade).count()
    elif current_user.role == "teacher":
        current_teacher = Teacher.query.join(User, User.username==Teacher.teacher_id).filter(User.username==current_user.username).first()
        student_class_count = Student.query.filter(Student.class_name==current_teacher.class_name, Student.major==current_teacher.major, Student.grade==current_teacher.grade).count()
    else:
        student_class_count = 0

    # 假设用户已登录，并且你能通过 current_user 获取到当前登录学生的 ID
    student_id = current_user.username  # 从用户表关联的 student_id 获取
    exam_with_scores_count = Score.query.filter_by(student_id=student_id).count() # 获取登录学生可查看的考试数

    return jsonify({
        'teacher_count': teacher_count,
        'student_count': student_count,
        'subject_count': subject_count,
        'exam_count': exam_count,
        'exam_with_scores_count': exam_with_scores_count,
        'student_class_count': student_class_count
    })
