from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from models import db, Notice

# 创建 notice 蓝图
notice = Blueprint('notice', __name__)

# 显示通知列表页面
@notice.route("/notice-list-html")
@login_required
def notice_list_html():
    return render_template('admin/notice-list.html')

# 显示添加通知页面
@notice.route("/add-notice-html")
@login_required
def add_notice_html():
    return render_template('admin/add-notice.html')

# 获取通知列表
@notice.route("/notices", methods=['GET'])
def get_notices():
    notices = Notice.query.all()
    data = [{
        'notice_id': n.notice_id,
        'content': n.content,
        'created_time': n.created_time.strftime('%Y-%m-%d %H:%M:%S'),
    } for n in notices]
    
    return jsonify(data)  # 将数据作为 JSON 响应返回

# 删除通知
@notice.route('/delete_notices', methods=['POST'])
def delete_notices():
    data = request.get_json()  # 获取请求中的 JSON 数据
    notice_ids = data.get('notice_ids', [])  # 提取通知 ID 列表

    if not notice_ids:
        return jsonify(success=False, message="未提供任何通知 ID！"), 400

    # 批量删除通知
    try:
        Notice.query.filter(Notice.notice_id.in_(notice_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True, message="删除成功！")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify(success=False, message="删除失败，请重试！", error=str(e)), 500

# 添加通知
@notice.route('/add_notice', methods=['POST'])
def add_notice():
    data = request.json
    notice_content = data.get('notice_content')
    if notice_content:
        new_notice = Notice(content=notice_content)
        db.session.add(new_notice)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="通知内容不能为空！"), 400
