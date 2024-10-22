from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from models import db, Score, SubjectScore

# 创建 score 蓝图
score = Blueprint('score', __name__)

@score.route('/import-score-html')
@login_required
def import_score_html():
    student_id = request.args.get('student_id')
    return render_template('admin/import-score.html', student_id=student_id)

@score.route('/import_score', methods=['POST'])
@login_required
def import_score():
    data = request.json
    student_id = data['student_id']
    exam_id = data['exam_id']
    scores = data['scores']

    # 检查学生是否已经导入了成绩
    existing_score = Score.query.filter_by(student_id=student_id, exam_id=exam_id).first()
    if existing_score:
        return jsonify({'message': '成绩已存在'})
    else:
        # 计算总成绩
        total_score = sum(int(score['value']) for score in scores)

        # 创建新的 Score 实例
        new_score = Score(student_id=student_id, exam_id=exam_id, total_score=total_score)

        # 将新成绩添加到数据库
        db.session.add(new_score)
        db.session.flush()  # 先执行插入操作以获取 score_id
        db.session.commit()  # 提交事务

        # 获取自动生成的 score_id
        score_id = new_score.score_id

        # 插入每个科目的成绩到 SubjectScore 表
        for score in scores:
            subject_score = SubjectScore(
                score_id=score_id,  # 使用刚刚插入的 score_id
                subject_id=score['subject_id'],  # 这里需要确保 subject_id 是正确的
                score=int(score['value'])
            )
            db.session.add(subject_score)

        db.session.commit()  # 提交所有的科目分数

        return jsonify({'message': '成绩导入成功'})

@score.route('/replace_score', methods=['POST'])
@login_required
def replace_score():
    data = request.json
    student_id = data['student_id']
    exam_id = data['exam_id']
    scores = data['scores']

    # 检查学生是否已经导入了成绩
    existing_score = Score.query.filter_by(student_id=student_id, exam_id=exam_id).first()
    if existing_score:
        existing_score.total_score = sum(int(score['value']) for score in scores)
        db.session.commit()  # 提交更新的成绩

        # 更新每个科目的成绩
        for score in scores:
            subject_score = SubjectScore.query.filter_by(score_id=existing_score.score_id, subject_id=score['subject_id']).first()
            if subject_score:
                # 如果存在则更新
                subject_score.score = int(score['value'])
            else:
                # 如果不存在则插入新的成绩
                subject_score = SubjectScore(
                    score_id=existing_score.score_id,
                    subject_id=score['subject_id'],
                    score=int(score['value'])
                )
                db.session.add(subject_score)

        db.session.commit()  # 提交所有的科目分数

        return jsonify({'message': '成绩已覆盖成功'})

