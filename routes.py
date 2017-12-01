from utils import log
from models.message import Message
from models.user import User


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
     主页的处理函数，返回主页的响应
    """
    header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'post':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登陆成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'post':
        """
         HTTP BODY username=qiu123&password=123 经过
         request.form()函数之后会变成一个字典
        """
        form = request.form()
        u = User.new(form)
        if u.validate_reginster():
            u.save()
            result = '注册成功<br><pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# message_list 存储了所有的message
message_list = []


def route_message(request):
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{message}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源处理函数，读取图片并且生成响应返回。
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}
