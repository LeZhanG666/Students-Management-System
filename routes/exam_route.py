from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Exam, Score, Student, Subject, ExamSubject, SubjectScore

# 创建 exam 蓝图
exam = Blueprint('exam', __name__)

# 显示管理员端考试列表页面
@exam.route("/admin-exam-list-html")
@login_required
def admin_exam_list_html():
    return render_template('admin/exam-list.html')

# 显示学生端考试列表页面
@exam.route("/student-exam-list-html")
@login_required
def student_exam_list_html():
    return render_template('student/exam-list.html')

# 显示试卷分析界面
@exam.route("/exam-analysis-html")
@login_required
def exam_analysis_html():
    return render_template('student/exam-analysis.html')

# 显示添加考试页面
@exam.route("/add-exam-html")
@login_required
def add_exam_html():
    return render_template('admin/add-exam.html')

# 获取考试列表
@exam.route('/admin_exams', methods=['GET'])
def admin_get_exams():
    exam_name = request.args.get("exam_name")
    exam_date = request.args.get("exam_date")
    page = int(request.args.get("page", 1))  # 当前页码，默认为第1页
    per_page = int(request.args.get("per_page", 10))  # 每页显示数量，默认为10

    # 初始化查询对象
    query = Exam.query

    # 根据筛选条件过滤
    if exam_name:
        query = query.filter(Exam.exam_name.like(f'%{exam_name}%'))  # 模糊查询
    if exam_date:
        query = query.filter(Exam.exam_date == exam_date)

    # 计算分页数据
    total = query.count()  # 总记录数
    exams = query.offset((page - 1) * per_page).limit(per_page).all()  # 分页查询

    # 将考试数据转换为JSON格式
    data = [
        {
            'exam_id': e.exam_id,
            'exam_name': e.exam_name,
            'exam_date': e.exam_date.isoformat()  # 转换为ISO格式
        }
        for e in exams
    ]

    return jsonify({
        'exams': data,
        'total': total,  # 返回总记录数以计算页数
        'page': page,
        'per_page': per_page
    })


# 获取问卷分析数据
@exam.route('/exam_analysis', methods=['GET'])
def exam_analysis():
    exam_id = request.args.get('exam_id', type=int)

    # 获取考试信息
    exam_info = Exam.query.filter_by(exam_id=exam_id).first()
    if not exam_info:
        return jsonify({"status": "error", "message": "考试不存在"}), 404

    # 获取该考试的所有成绩
    scores = Score.query.filter_by(exam_id=exam_id).all()
    total_participants = len(scores)

    # 计算平均分
    average_score = round(sum(score.total_score for score in scores) / total_participants, 2) if total_participants else 0

    # 获取登录者的学号
    student_id = current_user.username
    exam_all = db.session.query(Exam).join(Score).filter(Score.student_id == student_id).all()
    student_score = Score.query.filter_by(exam_id=exam_id, student_id=student_id).first().total_score

    # 获取学生的总体排名
    ranked_scores = Score.query.filter_by(exam_id=exam_id).order_by(Score.total_score.desc()).all()
    student_rank = next((index + 1 for index, score in enumerate(ranked_scores) if score.student_id == student_id), None)

    # 获取班级排名
    logged_in_student = Student.query.filter_by(student_id=student_id).first()
    if not logged_in_student:
        return jsonify({"status": "error", "message": "学生不存在"}), 404

    class_scores = Score.query.join(Student).filter(Student.class_name == logged_in_student.class_name, Score.exam_id == exam_id).all()
    class_total_participants = len(class_scores) # 该班所有总人数
    class_ranked_scores = sorted(class_scores, key=lambda x: x.total_score, reverse=True)
    class_rank = next((index + 1 for index, score in enumerate(class_ranked_scores) if score.student_id == student_id), None)

    # 获取最近五次考试的排名情况
    # recent_exams = Exam.query.order_by(Exam.exam_date.desc()).limit(5).all()
    recent_exams = Exam.query.filter(Exam.exam_id.in_([exam.exam_id for exam in exam_all])).order_by(Exam.exam_date.desc()).limit(5).all()
    overall_ranks = []
    class_ranks = []

    for exam in recent_exams:
        exam_scores = Score.query.filter_by(exam_id=exam.exam_id).all()
        exam_ranked_scores = sorted(exam_scores, key=lambda x: x.total_score, reverse=True)
        
        # 获取当前学生的总体排名
        overall_rank = next((index + 1 for index, score in enumerate(exam_ranked_scores) if score.student_id == student_id), None)
        overall_ranks.append(overall_rank)

        # 获取班级排名
        class_exam_scores = Score.query.join(Student).filter(Student.class_name == logged_in_student.class_name, Score.exam_id == exam.exam_id).all()
        class_ranked_scores = sorted(class_exam_scores, key=lambda x: x.total_score, reverse=True)
        class_rank = next((index + 1 for index, score in enumerate(class_ranked_scores) if score.student_id == student_id), None)
        class_ranks.append(class_rank)

    # 获取上次考试的名次提升情况
    previous_exam = Exam.query.filter(Exam.exam_date < exam_info.exam_date).order_by(Exam.exam_date.desc()).first()
    previous_rank = None
    if previous_exam:
        previous_student_score = Score.query.filter_by(exam_id=previous_exam.exam_id, student_id=student_id).first()
        if previous_student_score:
            previous_rank = next((index + 1 for index, score in enumerate(ranked_scores) if score.student_id == student_id), None)

    rank_improvement = (previous_rank - student_rank) if previous_rank and student_rank else None

    # 返回分析结果
    return jsonify({
        "status": "success",
        "total_participants": total_participants,
        "average_score": average_score,
        "student_score": student_score,
        "student_rank": student_rank,
        "class_total_participants": class_total_participants,
        "class_rank": class_rank,
        "rank_improvement": rank_improvement,
        "overall_ranks": overall_ranks,
        "class_ranks": class_ranks
    })


# 显示登录学生考试列表
@exam.route('/student_exams', methods=['GET'])
def student_get_exams():
    exam_name = request.args.get("exam_name")
    exam_date = request.args.get("exam_date")
    page = int(request.args.get("page", 1))  # 当前页码，默认为第1页
    per_page = int(request.args.get("per_page", 10))  # 每页显示数量，默认为10

    # 获取当前用户的 student_id
    student_id = current_user.username

    # 查询当前用户的成绩及对应的考试
    scores = Score.query.filter_by(student_id=student_id).all()
    exam_ids = [score.exam_id for score in scores]  # 获取有成绩的考试 ID 列表

    # 初始化查询对象
    query = Exam.query.filter(Exam.exam_id.in_(exam_ids))  # 筛选有成绩的考试

    # 根据筛选条件过滤
    if exam_name:
        query = query.filter(Exam.exam_name.like(f'%{exam_name}%'))  # 模糊查询
    if exam_date:
        query = query.filter(Exam.exam_date == exam_date)

    # 计算分页数据
    total = query.count()  # 总记录数
    exams = query.offset((page - 1) * per_page).limit(per_page).all()  # 分页查询

    # 将考试数据转换为JSON格式
    data = [
        {
            'exam_id': e.exam_id,
            'exam_name': e.exam_name,
            'exam_date': e.exam_date.isoformat()  # 转换为ISO格式
        }
        for e in exams
    ]

    return jsonify({
        'exams': data,
        'total': total,  # 返回总记录数以计算页数
        'page': page,
        'per_page': per_page
    })

# 显示考试排名页面
@exam.route('/exam/ranking', methods=['GET'])
def exam_ranking_page():
    exam_id = request.args.get('exam_id')

    if exam_id is None:
        return jsonify({"error": "缺少考试ID"}), 400
    
    # 查询考试信息
    exam = Exam.query.get(exam_id)
    if not exam:
        return jsonify({"error": "未找到该考试"}), 404

    # 渲染 HTML 页面
    if current_user.role == 'user':
        return render_template('admin/exam-ranking.html', exam=exam)
    else:
        return render_template('student/exam-ranking.html', exam=exam)


# 获取考试排名数据
@exam.route('/exam/ranking/data', methods=['GET'])
def get_exam_ranking():
    exam_id = request.args.get('exam_id')

    if not exam_id:
        return jsonify({"error": "缺少 exam_id 参数"}), 400
    # 获取考试信息
    exam = Exam.query.filter_by(exam_id=exam_id).first()
    if not exam:
        return jsonify({"error": "未找到该考试"}), 404

    # 获取考试相关科目列表
    subjects = Subject.query \
        .join(ExamSubject, ExamSubject.subject_id == Subject.subject_id) \
        .filter(ExamSubject.exam_id == exam_id).all()

    subjects_data = [{"subject_id": s.subject_id, "subject_name": s.subject_name} for s in subjects]

    # 查询学生及其总成绩，并获取单科成绩
    scores = Score.query.filter_by(exam_id=exam_id).all()
        
    student_scores = []
    for score in scores:
        student = Student.query.filter_by(student_id=score.student_id).first()

        # 获取该学生的每个科目成绩
        subject_scores = SubjectScore.query.filter_by(score_id=score.score_id).all()
        subject_score_data = [
            {"subject_id": s.subject_id, "score": s.score} for s in subject_scores
        ]

        student_scores.append({
            "student_id": student.student_id,
            "student_name": student.name,
            "class_name":student.class_name,
            "subject_scores": subject_score_data,
            "total_score": score.total_score
        })

    # 根据总成绩排序（降序）
    sorted_scores = sorted(student_scores, key=lambda x: x["total_score"], reverse=True)

    # 返回数据给前端
    return jsonify({
        "exam_name": exam.exam_name,
        "subjects": subjects_data,
        "scores": sorted_scores
    })

# 添加新考试
@exam.route('/add_exam', methods=['POST'])
def add_exam():
    data = request.json
    exam_name = data.get('exam_name')
    exam_date = data.get('exam_date')
    subjects = data.get('subjects', [])
    new_exam = Exam(exam_name=exam_name, exam_date=exam_date)
    db.session.add(new_exam)
    db.session.flush()  # 获取自增 ID

    # 添加到 exam_subjects 表
    for subject_id in subjects:
        exam_subject = ExamSubject(exam_id=new_exam.exam_id, subject_id=subject_id)
        db.session.add(exam_subject)

    db.session.commit()
    return jsonify({'success': True})

# 删除考试接口
@exam.route("/delete_exams", methods=["POST"])
def delete_exams():
    data = request.get_json()  # 获取请求中的 JSON 数据
    ids = data.get('ids', [])  # 提取考试 ID 列表

    if not ids:
        return jsonify(success=False, message="未提供任何考试 ID！"), 400

    # 批量删除考试
    try:
        Exam.query.filter(Exam.exam_id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True, message="删除成功！")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify(success=False, message="删除失败，请重试！", error=str(e)), 500
