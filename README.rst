QuantDigger 0.5.0 (Python 3.5)
==================


* qink:
    在原来0.5.0版的基础上改为支持Python3.5    2017-07-13


依赖库
-------
* Python (仅在3.5上进行测试, **2.7请找原版**)
* matplotlib 
* numpy
* logbook
* pandas 
* progressbar2
* zmq
* BeautifulSoup4 (tushare需要)
* lxml (tushare需要)
* tushare_ (一个非常强大的股票信息抓取工具)
* python-dateutil(可选)
* pyqt (可选)
* Pyqt (可选)
* IPython (可选)
* TA-Lib

* 可以用pip安装依赖库:
    >>> pip install -r requirements.txt --upgrade
* 如果出现pypi源超时情况:
    >>> pip install -r requirements.txt --upgrade -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

* TA-Lib 通过pip直接安装可能会出错，
    * 到 http://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下载相应版本然后通过命令安装，如
        >>> pip install TA_Lib-0.4.10-cp35-cp35m-win_amd64.whl
    * Anaconda用户可以用
        >>> conda install -c quantopian ta-lib


策略组合DEMO
-----------

源码
~~~~

.. code:: py


    #from quantdigger.engine.series import NumberSeries
    #from quantdigger.indicators.common import MA
    #from quantdigger.util import  pcontract
    from quantdigger import *

    class DemoStrategy(Strategy):
        """ 策略A1 """
    
        def on_init(self, ctx):
            """初始化数据""" 
            ctx.ma10 = MA(ctx.close, 10, 'ma10', 'y', 2)
            ctx.ma20 = MA(ctx.close, 20, 'ma20', 'b', 2)

        def on_symbol(self, ctx):
            """  选股 """ 
            return

        def on_bar(self, ctx):
            if ctx.curbar > 20:
                if ctx.ma10[2] < ctx.ma20[2] and ctx.ma10[1] > ctx.ma20[1]:
                    ctx.buy(ctx.close, 1) 
                elif ctx.pos() > 0 and ctx.ma10[2] > ctx.ma20[2] and \
                     ctx.ma10[1] < ctx.ma20[1]:
                    ctx.sell(ctx.close, ctx.pos()) 

        def on_exit(self, ctx):
            return

    class DemoStrategy2(Strategy):
        """ 策略A2 """
    
        def on_init(self, ctx):
            """初始化数据""" 
            ctx.ma5 = MA(ctx.close, 5, 'ma5', 'y', 2) 
            ctx.ma10 = MA(ctx.close, 10, 'ma10', 'black', 2)

        def on_symbol(self, ctx):
            """  选股 """ 
            return

        def on_bar(self, ctx):
            if ctx.curbar > 10:
                if ctx.ma5[2] < ctx.ma10[2] and ctx.ma5[1] > ctx.ma10[1]:
                    ctx.buy(ctx.close, 1) 
                elif ctx.pos() > 0 and ctx.ma5[2] > ctx.ma10[2] and \
                     ctx.ma5[1] < ctx.ma10[1]:
                    ctx.sell(ctx.close, ctx.pos()) 

        def on_exit(self, ctx):
            return

    if __name__ == '__main__':
        set_symbols(['BB.SHFE-1.Minute'], 0)
        # 创建组合策略
        # 初始资金5000， 两个策略的资金配比为0.2:0.8
        profile = add_strategy([DemoStrategy('A1'), DemoStrategy2('A2')], { 'captial': 5000,
                                  'ratio': [0.2, 0.8] })
        run()

        # 绘制k线，交易信号线
        from quantdigger.digger import finance, plotting
        plotting.plot_strategy(profile.data(0), profile.indicators(1), profile.deals(1))
        # 绘制策略A1, 策略A2, 组合的资金曲线
        curve0 = finance.create_equity_curve(profile.all_holdings(0))
        curve1 = finance.create_equity_curve(profile.all_holdings(1))
        curve = finance.create_equity_curve(profile.all_holdings())
        plotting.plot_curves([curve0.equity, curve1.equity, curve.equity],
                            colors=['r', 'g', 'b'],
                            names=[profile.name(0), profile.name(1), 'A0'])
        # 绘制净值曲线
        plotting.plot_curves([curve.networth])
        # 打印统计信息
        print finance.summary_stats(curve, 252*4*60)


策略结果
~~~~~~~

* k线和信号线

k线显示使用了系统自带的一个联动窗口控件，由蓝色的滑块控制显示区域，可以通过鼠标拖拽改变显示区域。
`上下方向键` 来进行缩放。 

  .. image:: doc/images/plot.png
     :width: 500px

* 2个策略和组合的资金曲线。
  
  .. image:: doc/images/figure_money.png
     :width: 500px

* 组合的历史净值
  
  .. image:: doc/images/figure_networth.png
     :width: 500px

* 统计结果

::
       
    >>> [('Total Return', '-0.99%'), ('Sharpe Ratio', '-5.10'), ('Max Drawdown', '1.72%'), ('Drawdown Duration', '3568')]


.. _TeaEra: https://github.com/TeaEra
.. _deepfish: https://github.com/deepfish
.. _wondereamer: https://github.com/wondereamer
.. _HonePhy: https://github.com/HonePhy
.. _tushare: https://github.com/waditu/tushare
.. _Jimmy: https://github.com/jimmysoa
.. _vodkabuaa: https://github.com/vodkabuaa
.. _ongbe: https://github.com/ongbe
.. _pyalgotrade: https://github.com/gbeced/pyalgotrade
.. _zipline: https://github.com/quantopian/zipline
.. _wiki文档: https://github.com/QuantFans/quantdigger/wiki


版本
~~~~
**0.5.0 版本 2017-07-13**

* 在原来0.5.0版的基础上改为支持Python3.5

**0.5.0 版本 2017-01-08**

* 完善文档
* 数据源可配置
* 添加shell, 界面，回测引擎三则间的交互框架

**0.3.0 版本 2015-12-09**

* 重新设计回测引擎, 支持组合回测，选股
* 重构数据模块

**0.2.0 版本 2015-08-18**

* 修复股票回测的破产bug
* 修复回测权益计算bug
* 交易信号对的计算从回测代码中分离
* 把回测金融指标移到digger/finace
* 添加部分数据结构，添加部分数据结构字段
* 添加几个mongodb相关的函数
    
**0.1.0 版本 2015-06-16**

* 夸品种的策略回测功能
* 简单的交互
* 指标，k线绘制
