from flask import Flask, request, jsonify, make_response
from models import User, Payment

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    """注册用户"""
    # 获取请求参数
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    # 创建 User 对象并保存到数据库
    user = User(username=username, password=password, email=email)
    user.save()

    return jsonify({
        'success': True,
        'message': '注册成功',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'trial_end_date': user.trial_end_date,
            'trial_max_count': user.trial_max_count,
            'trial_max_chars': user.trial_max_chars,
            'avatar_path': user.avatar_path
        }
    })


@app.route('/login', methods=['POST'])
def login():
    """用户登录"""

    # 获取请求参数
    username = request.form.get('username')
    password = request.form.get('password')

    # 根据用户名查找用户
    user = User.find_by_username(username)

    # 判断用户是否存在和密码是否正确
    if user and user.password == password:
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'trial_end_date': user.trial_end_date,
                'trial_max_count': user.trial_max_count,
                'trial_max_chars': user.trial_max_chars,
                'avatar_path': user.avatar_path
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        })


@app.route('/account', methods=['GET'])
def account():
    """获取用户信息"""
    # 获取请求参数
    user_id = request.args.get('user_id')

    # 根据用户 ID 查找用户
    user = User.find_by_id(user_id)

    # 判断用户是否存在
    if user:
        return jsonify({
            'success': True,
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'trial_end_date': user.trial_end_date,
                'trial_max_count': user.trial_max_count,
                'trial_max_chars': user.trial_max_chars,
                'avatar_path': user.avatar_path
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })


@app.route('/trial', methods=['POST'])
def trial():
    """试用"""
    # 获取请求参数
    user_id = request.form.get('user_id')
    count = request.form.get('count')
    chars = request.form.get('chars')

    # 根据用户 ID 查找用户
    user = User.find_by_id(user_id)

    # 判断用户是否存在和试用是否已过期
    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })
    elif user.trial_end_date and user.trial_end_date < User.current_date():
        return jsonify({
            'success': False,
            'message': '试用已过期'
        })

    # 判断试用次数和字符数是否已用完
    if user.trial_max_count is not None and int(count) > user.trial_max_count:
        return jsonify({
            'success': False,
            'message': '试用次数已用完'
        })
    elif user.trial_max_chars is not None and int(chars) > user.trial_max_chars:
        return jsonify({
            'success': False,
            'message': '试用字符数已用完'
        })

    # 更新用户试用信息
    user.trial_end_date = User.trial_end_date()
    user.save()

    return jsonify({
        'success': True,
        'message': '试用成功',
        'data': {
            'trial_end_date': user.trial_end_date
        }
    })


@app.route('/payment', methods=['POST'])
def payment():
    """支付"""
    # 获取请求参数
    user_id = request.form.get('user_id')
    payment_type = request.form.get('payment_type')
    payment_amount = request.form.get('payment_amount')

    # 根据用户 ID 查找用户
    user = User.find_by_id(user_id)

    # 判断用户是否存在
    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })

    # 创建 Payment 对象并保存到数据库
    payment = Payment(user_id=user.id, payment_type=payment_type, payment_amount=payment_amount)
    payment.save()

    # 更新用户信息
    user.update_payment_info(payment)

    return jsonify({
        'success': True,
        'message': '支付成功',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'trial_end_date': user.trial_end_date,
            'trial_max_count': user.trial_max_count,
            'trial_max_chars': user.trial_max_chars,
            'avatar_path': user.avatar_path,
            'payment_id': payment.id,
            'payment_type': payment.payment_type,
            'payment_amount': payment.payment_amount,
            'payment_date': payment.payment_date
        }
    })

if __name__ == '__main__':
    app.run(debug=True)