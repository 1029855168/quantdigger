# -*- coding: utf8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from quantdigger.widgets.mplotwidgets import widgets, mplots
from quantdigger.digger import finance
from matplotlib.ticker import Formatter

def xticks_to_display(data_length):
    #print(r.index[0].weekday())
    interval = data_length / 5
    v = 0
    xticks = []
    for i in range(0, 6):
        xticks.append(v)
        v += interval
    return xticks


def plot_result(price_data, indicators, signals,
        all_holdings):
    """ 
        显示回测结果。
    """
    print "summary.." 
    curve = finance.create_equity_curve_dataframe(all_holdings)
    print finance.output_summary_stats(curve)

    print "plotting.."
    fig = plt.figure()
    frame = widgets.MultiWidgets(fig, price_data,
                                50         # 窗口显示k线数量。
                                #4, 1     # 两个1:1大小的窗口
                                )

    # 添加k线
    kwindow = widgets.CandleWindow("kwindow", price_data, 100, 50)
    frame.add_widget(0, kwindow, True)
    ## 交易信号。
    signal = mplots.TradingSignalPos(price_data, signals, lw=2)
    frame.add_indicator(0, signal)
    ## @bug indicators导致的双水平线!
    ## @todo 完mplot_demo上套。
    #frame.add_indicator(0, Volume(None, price_data.open, price_data.close, price_data.volume))

    ## 添加指标
    for name, indic in indicators.iteritems():
        frame.add_indicator(0, indic)

    frame.draw_widgets()
    
    # 画资金曲线
    #print curve.equity
    fig2 = plt.figure()
    ax = fig2.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.xaxis.set_major_formatter(TimeFormatter(curve.index, '%Y-%m-%d' ))
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    #ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.set_xticks(xticks_to_display(len(curve)))
    ax.plot(curve.equity)
    plt.show()


class TimeFormatter(Formatter):
    #def __init__(self, dates, fmt='%Y-%m-%d'):
    # 分类 －－format
    def __init__(self, dates, fmt='%Y-%m-%d %H:%M'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(round(x))
        if ind>=len(self.dates) or ind<0: return ''

        return self.dates[ind].strftime(self.fmt)
