from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    username = db.Column(db.String(20), db.ForeignKey('students.student_id'), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)


class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('男', '女'), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('男', '女'), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

class Exam(db.Model):
    __tablename__ = 'exams'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)

class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(100), nullable=False)

class ExamSubject(db.Model):
    __tablename__ = 'examsubjects'
    exam_subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.exam_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)

class Score(db.Model):
    __tablename__ = 'scores'
    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.exam_id'), nullable=False)
    total_score = db.Column(db.Float, nullable=False)

class SubjectScore(db.Model):
    __tablename__ = 'subjectscores'
    subject_score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score_id = db.Column(db.Integer, db.ForeignKey('scores.score_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    score = db.Column(db.Float, nullable=False)

class Notice(db.Model):
    __tablename__ = 'notices'
    notice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))