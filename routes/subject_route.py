from flask import Blueprint, request, jsonify
from models import db, Subject, ExamSubject

# 创建 subject 蓝图
subject = Blueprint('subject', __name__)

# 获取考试的科目列表
@subject.route('/exams/<int:exam_id>/subjects')
def get_exam_subjects(exam_id):
    subjects = (
        db.session.query(Subject)
        .join(ExamSubject, ExamSubject.subject_id == Subject.subject_id)
        .filter(ExamSubject.exam_id == exam_id)
        .all()
    )
    return jsonify({
        'subjects': [
            {
                'subject_name': subject.subject_name,
                'subject_id': subject.subject_id
            }
            for subject in subjects
        ]
    })

# 获取已有科目列表
@subject.route('/get_subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    subject_list = [{"subject_id": s.subject_id, "subject_name": s.subject_name} for s in subjects]
    return jsonify({"data": subject_list})

# 添加新科目
@subject.route('/add_subject', methods=['POST'])
def add_subject():
    subject_name = request.form.get('subject_name')
    existing_subject = Subject.query.filter_by(subject_name=subject_name).first()
    if subject_name:
        if existing_subject:
            return jsonify({"success": False, "message": '该科目已经存在，请重试！'})      
        new_subject = Subject(subject_name=subject_name)
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({"success": True, "message": '添加成功'})
    return jsonify({"success": False, "message": '添加失败，请重试'})

# 删除科目
@subject.route('/delete_subjects', methods=['POST'])
def delete_subjects():
    data = request.get_json()  # 获取请求中的 JSON 数据
    ids = data.get('subject_ids', [])  # 提取科目 ID 列表

    if not ids:
        return jsonify(success=False, message="未提供任何科目 ID！"), 400

    # 批量删除科目
    try:
        Subject.query.filter(Subject.subject_id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True, message="删除成功！")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify(success=False, message="删除失败，请重试！", error=str(e)), 500
