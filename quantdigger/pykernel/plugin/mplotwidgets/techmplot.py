# -*- coding: utf8 -*-
from matplotlib.widgets import Cursor
from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt
import widgets


import os, sys
sys.path.append(os.path.join('..', '..'))
from datasource.data import get_stock_signal_data
price_data, entry_x, entry_y, exit_x, exit_y, colors = get_stock_signal_data()

import datetime
import numpy as np
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def moving_average_convergence(x, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow

rsi = relative_strength(price_data['close'])
def plot_rsi(ax, fillcolor = 'b'):
    """docstring for plot_rsi""" 
    textsize = 9
    ax.plot(rsi, color=fillcolor)
    ax.axhline(70, color=fillcolor)
    ax.axhline(30, color=fillcolor)
    ax.fill_between(rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
    ax.fill_between(rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
    ax.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax.transAxes, fontsize=textsize, color = 'k')
    ax.text(0.6, 0.1, '<30 = oversold', transform=ax.transAxes, fontsize=textsize, color = 'k')
    ax.set_ylim(0, 100)
    ax.set_yticks([30,70])
    ax.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax.transAxes, fontsize=textsize)


#plt.rc('axes', grid=True)





class TechMPlot(object):
    def __init__(self, fig, *args):
        self.fig = fig
        self.cross_cursor = None
        self.v_cursor = None
        self.in_qt = False
        self.left, self.width = 0.1, 0.8
        self.add_subplot(*args)
        for ax in self.axes:
            ax.format_coord = self.format_coord 
        self.connect()

    def init_qt(self):
        """docstring for set_qt""" 
        self.in_qt = True
        if len(self.axes) == 1:
            self.cross_cursor = Cursor(self.axes[0], useblit=True, color='red', linewidth=2, vertOn=True, horizOn=True)
        else:
            self.v_cursor = MultiCursor(self.fig.canvas, self.axes, color='r', lw=2, horizOn=False, vertOn=True)

    def connect(self):
        """
        matplotlib信号连接。
        """
        #self.cidpress = self.fig.canvas.mpl_connect( "button_press_event", self.on_press)
        #self.cidrelease = self.fig.canvas.mpl_connect( "button_release_event", self.on_release)
        #self.cidmotion = self.fig.canvas.mpl_connect( "motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect('axes_enter_event', self.enter_axes)
        self.fig.canvas.mpl_connect('axes_leave_event', self.leave_axes)

        self.slider.connect()
        self.kwindow.connect()


    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cidmotion)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidpress)


    def on_press(self, event):
        pass

    def on_release(self, event):
        pass

    def on_motion(self, event):
        #self.fig.canvas.draw()
        pass

    def enter_axes(self, event):
        #event.inaxes.patch.set_facecolor('yellow')
        # 只有当前axes会闪烁。
        if event.inaxes is self.slider_ax or self.in_qt or event.inaxes is self.range_ax:
            return 
        axes = [ax for ax in self.axes if ax is not event.inaxes]
        if len(axes) > 1:
            self.v_cursor = MultiCursor(event.canvas, axes, color='r', lw=2, horizOn=False, vertOn=True)
        self.cross_cursor = Cursor(event.inaxes, useblit=True, color='red', linewidth=2, vertOn=True, horizOn=True)
        event.canvas.draw()
        print("enter---")

    def leave_axes(self, event):
        if not self.in_qt:
            self.v_cursor = None
            self.cross_cursor = None
            event.canvas.draw()  # 在qt中不起作用，还影响流畅。
        print("leave---")

    def add_subplot(self, *args):
        args = list(reversed(args))
        bottom = 0.1
        self.slider_ax = self.fig.add_axes([self.left, 0.05, self.width, 0.1])
        self.range_ax = self.fig.add_axes([self.left, 0.6, self.width, 0.3],
                zorder = 0, frameon=False, sharex=self.slider_ax, visible=False)


        self.slider = widgets.Slider(self.slider_ax, "slider", '', 0, len(price_data),
                                    len(price_data), len(price_data)/50, "%d")

        num_axes = sum(args)
        unit = (1.0 - bottom) / num_axes
        for i, ratio in enumerate(args):
            rect = [self.left, bottom, self.width, unit * ratio]
            if i > 0:
                print len(self.axes)
                print len(self.fig.axes)
                self.fig.add_axes(rect, sharex=self.axes[0])  #axisbg=axescolor)
            else:
                self.fig.add_axes(rect)
            bottom += unit * ratio

        for ax in self.axes:
            ax.grid(True)
            ax.set_xticklabels([])
        main_index = -1 if len(self.axes) > 1 else 0
        self.kwindow = widgets.CandleWindow(self.axes[main_index], "kwindow", price_data, 100, 50)


        plot_rsi(self.axes[-2])
        ma20 = moving_average(price_data['close'], 20, type='simple')
        ma30 = moving_average(price_data['close'], 30, type='simple')
        linema20, = self.axes[-1].plot( ma20, color='y', lw=2, label='MA (20)')
        linema30, = self.axes[-1].plot( ma30, color='b', lw=2, label='MA (30)')
        props = font_manager.FontProperties(size=10)
        leg = self.axes[-1].legend(loc='center left', shadow=True, fancybox=True, prop=props)
        leg.get_frame().set_alpha(0.5)
    


        #volume = (r.close*r.volume)/1e6  # dollar volume in millions
        ax2t = self.axes[0]
        volume = price_data['vol']
        #vmax = volume.max()
        finance.volume_overlay(ax2t, price_data['open'], price_data['close'],
                price_data['vol'], colorup = 'r', colordown = 'b', width = 1)
        #poly = ax2t.fill_between(volume, 0, label='Volume', facecolor='b', edgecolor='b' )
        #ax2t.set_ylim(0, 5*vmax)
        #ax2t.set_yticks([])


        self.rangew = widgets.RangeWidget('range', self.range_ax, price_data['close'])
        self.slider.add_observer(self.kwindow)
        self.slider.add_observer(self.rangew)
        self.signal = widgets.SignalWindow(self.axes[main_index], zip(zip(entry_x,entry_y),zip(exit_x,exit_y)), colors, 2)


    def subplots_adjust(self, left, bottom, right, top, wspace=None, hspace=None):
        plt.subplots_adjust(left, bottom, right, top, wspace, hspace)

    @property
    def axes(self):
        """ 返回滚动条以外的区域 """
        return self.fig.axes[2:]

    def format_coord(self, x, y):
        """ 状态栏信息显示 """
        index = x
        f = x % 1
        index = x-f if f < 0.5 else x-f+1
        #print len(self.kwindow.rects.get_array())
        return "pos=%d o=%.2f c=%.2f h=%.2f l=%.2f" % (index,
                price_data['open'][index], price_data['close'][index], price_data['high'][index],
                price_data['low'][index])

    def draw_axes(self, ith, func):
        """传递绘图函数，画第ith个图。
        
        Args:
            ith (number): 待绘axes的编号。
            func (function): 绘图函数。
        """
        try:
            axes = self.axes[ith]
        except IndexError as e:
            print(e)
        else:
            func(axes)

