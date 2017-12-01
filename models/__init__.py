import json
"""
 使用json格式序列化/反序列化字典或者列表
"""


from utils import log


def save(data, path):
    """
    本函数把一个dict或者list写入文件
    data为dict或者list path是保存文件的路径
    """
    # indent是缩进 ensure_ascii=False用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并且赚翻为dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


# Model是用于存储数据的基类
class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        # 得到一个类的所有存储实例
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        # save函数用于把一个Model的实例保存到文件中
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__是包含了对象的所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: {{}}'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)