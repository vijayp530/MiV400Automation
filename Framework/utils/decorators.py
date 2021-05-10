import logging

log = logging.getLogger("boss_api.deco")
def func_logger(F):
    def wrapper(*args, **kwargs):
        try:
            log.info('Called {0} with {1}'.format(F.__name__,args[1:]))
            return F(*args, **kwargs)
        except Exception as e:
            log.error('Called {0} {1} and got exception <{3}>.Exception msg <{2}>'.format(F.__name__, args, e.message, e.__class__))
            # raise Exception(e)
    return wrapper

@func_logger
def func(x, y):
    return ( x/y )

class C(object):
    @func_logger
    def fun(self, x, y):
        log.info( x-y )

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    c = C()
    c.fun(11,2)
    print(func(33,3))