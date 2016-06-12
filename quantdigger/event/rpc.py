# encoding: UTF-8
##
# @file eventenvine.py
# @brief 
# @author wondereamer
# @version 0.1
# @date 2016-05-17
import time
import json
import zmq  
from datetime import datetime
from threading import Thread, Condition, Lock
from quantdigger.util import elogger as log
from quantdigger.errors import InvalidRPCClientArguments
from quantdigger.event.eventengine import Event


class RPCServer(object):
    def __init__(self):
        self._routes = { }
        self._routes_lock = Lock()

    def _process_request(self, event):
        pass


    def register(self, route, handler):
        """ 注册服务函数。
        
        Args:
            route (str): 服务名
            handler (function): 回调函数
        
        Returns:
            Bool. 是否注册成功。
        """
        if route in self._routes:
            return False 
        with self._routes_lock:
            self._routes[route] = handler
        return True

    def unregister(self, route):
        """ 注销服务函数 """
        with self._routes_lock:
            if route in self._routes:
                del self._routes[route]


class EventRPCClient(object):
    def __init__(self, event_engine, service, event_client=None, event_server=None):
        self.EVENT_CLIENT = event_client if event_client else "%s_CLIENT" % service.upper()
        self.EVENT_SERVER = event_server if event_server else "%s_SERVER" % service.upper()
        self.rid = 0
        self._handlers = { }
        self._handlers_lock = Lock()
        self._event_engine = event_engine
        self._event_engine.register(self.EVENT_SERVER, self._process_apiback)
        self._pause_condition = Condition()
        self._sync_ret = None
        self._timeout = 0
        self._timer_sleep = 1
        self._sync_call_time_lock = Lock()
        self._sync_call_time = datetime.now()
        timer = Thread(target = self._run_timer)
        timer.daemon = True
        timer.start()

    def _run_timer(self):
        while True:
            if not self._timeout == 0:
                with self._sync_call_time_lock:
                    mtime = self._sync_call_time
                delta = (datetime.now()-mtime).seconds
                if delta >= self._timeout:
                    #print "timeout", self._timeout, delta
                    # 不可重入，保证self.rid就是超时的那个
                    with self._handlers_lock:
                        del self._handlers[self.rid]
                    log.debug("[RPCClient._runtimer] 处理超时, delete rid; %s" % self.rid)
                    self._timeout = 0
                    self._notify_server_data()
            time.sleep(self._timer_sleep)

    def _process_apiback(self, event):
        assert(event.route == self.EVENT_SERVER)
        self._timeout = 0
        rid = event.args['rid']
        #print rid, "**" 
        try:
            with self._handlers_lock:
                handler = self._handlers[rid]
        except KeyError:
            log.info('[RPCClient._process_apiback] 放弃超时任务的返回结果')
        else:
            try:
                if handler:
                    handler(event.args['ret'])
                else:
                    self._sync_ret = event.args['ret']
                    self._notify_server_data()
            except Exception as e:
                print e
            log.debug("[RPCClient._process_apiback] 删除已经完成的任务 rid; %s" % rid)
            with self._handlers_lock:
                del self._handlers[rid]

    def call(self, apiname, args, handler):
        """ 给定参数args，异步调用RPCServer的apiname服务,
        返回结果做为回调函数handler的参数。
        
        Args:
            apiname (str): 服务API名称。
            args (dict): 给服务API的参数。
            handler (function): 回调函数。
        """
        if not isinstance(args, dict):
            raise InvalidRPCClientArguments(argtype=type(args))
        assert(not handler ==  None)
        self.rid += 1
        args['apiname'] = apiname
        args['rid'] = self.rid
        self._event_engine.emit(Event(self.EVENT_CLIENT, args))
        with self._handlers_lock:
            self._handlers[self.rid] = handler

    def sync_call(self, apiname, args, timeout=10):
        """ 给定参数args，同步调用RPCServer的apiname服务,
        返回该服务的处理结果。如果超时，返回None。
        
        Args:
            apiname (str): 服务API名称。
            args (dict): 给服务API的参数。
            handler (function): 回调函数。
        """
        log.debug('sync_call: %s', apiname)
        if not isinstance(args, dict):
            self._timeout = 0
            self._sync_ret = None
            raise InvalidRPCClientArguments(argtype=type(args))
        self.rid += 1
        args['apiname'] = apiname
        args['rid'] = self.rid
        with self._sync_call_time_lock:
            self._sync_call_time = datetime.now()
        self._timeout = timeout
        self._event_engine.emit(Event(self.EVENT_CLIENT, args))
        with self._handlers_lock:
            self._handlers[self.rid] = None
        self._waiting_server_data()
        ret = self._sync_ret
        self._sync_ret = None
        return ret

    def _waiting_server_data(self):
        with self._pause_condition:
            self._pause_condition.wait()

    def _notify_server_data(self):
        with self._pause_condition:
            self._pause_condition.notify()


class EventRPCServer(RPCServer):
    def __init__(self, event_engine, service, event_client=None, event_server=None):
        super(EventRPCServer, self).__init__()
        self.EVENT_CLIENT = event_client if event_client else "%s_CLIENT" % service.upper()
        self.EVENT_SERVER = event_server if event_server else "%s_SERVER" % service.upper()
        self._event_engine = event_engine
        self._event_engine.register(self.EVENT_CLIENT, self._process_request)

    def _process_request(self, event):
        #print "rpcsever: ", event.route, event.args
        args = event.args
        rid = args['rid']
        apiname = args['apiname']
        del args['rid']
        del args['apiname']
        log.debug('RPCServer process: %s' % apiname)
        try:
            with self._routes_lock:
                handler = self._routes[apiname]
            ret = handler(args)
        except Exception as e:
            print e, "****" 
        else:
            args = { 'ret': ret,
                    'rid': rid
            }
            log.debug('RPCServer emit')
            self._event_engine.emit(Event(self.EVENT_SERVER, args))


class ZMQRPCServer(RPCServer):
    """docstring for ZMQRPCServer"""
    def __init__(self):
        super(ZMQRPCServer, self).__init__()
        self._context = zmq.Context()  
        self._socket = self._context.socket(zmq.REP)  
        self._socket.bind("tcp://*:5555")  
        #worker = Thread(target = self._process_request)
        ### @todo maybe remove daemon
        #worker.daemon = True
        #worker.start()
        self._process_request()

    def _process_request(self):
        while True:  
            #  Wait for next request from client  
            message = self._socket.recv()  
            message = json.loads(message)
            log.debug('RPCServer process: %s' % message['apiname'])
            try:
                with self._routes_lock:
                    handler = self._routes[message['apiname']]
                ret = handler(message['data'])
            except Exception as e:
                print e, "****" 
            else:
                log.debug('RPCServer emit')
                ret = json.dumps(ret)
                self._socket.send(ret)


class ZMQRPCClient(object):
    """docstring for ZMQRPCClient"""
    def __init__(self):
        print "Connecting to hello world server..."  
        self._context = zmq.Context()  
        self._socket = self._context.socket(zmq.REQ)  
        self._socket.connect ("tcp://localhost:5555")  

    def call(self, apiname, args, handler):
        pass

    def sync_call(self, apiname, args, timeout=10):
        data = {
            'apiname': apiname,
            'data': args
        }
        self._socket.send(json.dumps(data))  

        message = self._socket.recv()  
        ret = json.loads(message)
        return ret


if __name__ == '__main__':

    def print_hello(self, data):
        """""" 
        print "hello" 
        print data
        return "123"

    server = ZMQRPCServer()
    #server.register("print_hello", print_hello)
    time.sleep(1000)
