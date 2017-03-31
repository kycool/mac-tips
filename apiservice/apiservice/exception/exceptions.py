# -*- coding: utf-8 -*-

from django.utils.encoding import force_text

EXCEPTION_PHRASES = {
    '40000': 'common error message',

    # 40001 -- 40100 文章类型中的业务码
    '40001': '指定的分类不存在',

    # 40101 -- 40200 分类类型中的业务码

    # 40201 -- 40300 标签类型中的业务码
    '40201': '指定的标签不存在',

    # 40201 -- 40300 配置类型中的业务码

    # 40201 -- 40300 其他类型中的业务码

    # 数据库处理错误
    '41001': '数据库事务处理异常',
}


class BusinessException(Exception):
    default_error_code = "9000"
    default_error_message = "系统错误"

    def __init__(self, error_code=None, error_message=None, error_data=None):
        if error_code is not None and error_message is not None:
            self.error_code = error_code
            self.error_message = error_message
        elif error_code is not None:
            self.error_code = error_code
            self.error_message = force_text(EXCEPTION_PHRASES.get(error_code))
        else:
            self.error_code = self.default_error_code
            self.error_message = force_text(self.default_error_message)

        if error_data:
            self.error_data = error_data

    def __str__(self):
        return self.error_message
