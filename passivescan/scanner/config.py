# coding:utf8
__author__ = 'hartnett'

# mongodb 配置项
db_info = dict(
    host="127.0.0.1",
    port=27017,
    username="xsec",
    password="x@xsec.io"
)

CONST_WHITE_DOMAINS = ['weibo.com', 'sina.com.cn', 'google.com', 'baidu.com', 'cnzz.com']

CONST_REDIS = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 1,
    'password' : 'x@xsec.io'
}

REDIS_SERVER = "redis://:%s@%s:%d/%d" % (
    CONST_REDIS.get('password'),
    CONST_REDIS.get('host'),
    CONST_REDIS.get('port'),
    CONST_REDIS.get('db')
)

BROKER_URL = REDIS_SERVER
BACKEND_URL = REDIS_SERVER
