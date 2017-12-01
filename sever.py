import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


# 定义一个class用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        form函数用于把body解析为一个字典后返回
        body格式为 a=b&c=d&e=f
        """
        # TODO应该在解析出数据后再去unquote

        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def error(request, code=404):
    """
    根据code返回不同的错误响应 暂定404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    解析路径示例：
    message=hello&author=qiu
    {
        'message': 'hello',
        'author': 'qiu'
    }
    用于把path和query分离
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and  query', path, query)
    """
    根据path调用响应处理函数，若没有处理的path会调用error函数，返回404.
    """
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    使用with保证程序中断的时候正确关闭
    """
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            log('原始请求', r)
            # chrome可能会发送空请求导致split得到空list，判断防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置request的method
            request.method = r.split()[0]
            # 设置request的body
            request.body = r.split('\r\n\r\n', 1)[1]
            # 调用response_for_path函数得到path对应响应内容
            response = response_for_path(path)
            # 响应发给客户端
            connection.sendall(response)
            # 处理完成关闭连接
            connection.close()


if __name__=='__main__':
    # 生产配置并且运行程序
    config = {
        'host': '',
        'port': 3000,
    }
    run(**config)

