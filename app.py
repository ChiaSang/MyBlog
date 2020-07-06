# -*- coding:utf-8 -*-
# base.html为基本html，主体框架，其他页面继承自这个页面
# navbar.html 导航页
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from markupsafe import escape
# from flask import Flask, render_template, request, redirect, url_for
from Apps import create_app
from Apps.user.model import User
from Apps.article.model import *
from extents import db

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

from flask_bootstrap import Bootstrap
# import settings

# app = Flask(__name__)
# bootstrap = Bootstrap(app)
# app.config.from_object(settings)

name = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}

p_name = ['京东商城', '苏宁电器', '国美', '淘宝', '天猫', '亚马逊', '聚划算', '爱淘宝', '网易考拉', '网易严选', '阿里云', '优酷', '爱奇艺', '腾讯视频', '芒果TV',
          '乐视视频', '搜狐视频', '哔哩哔哩', '土豆网', 'CCTV', '斗鱼直播', '虎牙直播', 'YY直播', '企鹅电竞', '企鹅直播', '直播吧', '花椒直播', '战旗直播', '龙珠直播',
          '凤凰网', '环球网', '澎湃新闻', '腾讯新闻', '新浪新闻', '搜狐新闻', '网易新闻', '观察者', '军事头条', '中华网军事', '铁血军事', '腾讯军事', '人民网军事', '米尔网',
          '新浪军事', '环球军事', '凤凰军事', '东方财富', '新浪财经', '和讯财经', '第一财经', '财新网', '中国经济网', '网易财经', '证券之星', '雪球财经', '新浪微博', '知乎',
          '豆瓣', '百度贴吧', 'LOFTER', '水木社区', '天涯社区', '猫扑网', 'Dribbble', 'Iconfont', 'Easyicon', '花瓣网', '摄图网', '包图网',
          '网易云音乐', 'QQ音乐', '酷狗音乐', '荔枝FM', '蜻蜓FM', '酷我音乐', '虾米音乐', '喜马拉雅', '豆瓣FM', '携程网', '飞猪旅行', '马蜂窝', '途牛', '穷游网',
          '驴妈妈', '同程网', '去哪儿', 'NBA', 'CCTV5', '网易体育', '直播吧', '懂球帝', '虎扑体育', '新浪体育', '腾讯体育', '搜狐体育', '汽车之家', '太平洋汽车',
          '易车网', '人人车', '优信二手车', '瓜子二手车', '爱卡汽车', '车辆违章查询', '汽车用品', '哔哩哔哩', 'M站', '腾讯动漫', '网易漫画', '半次元', '有妖气', '中关村在线',
          '太平洋电脑', 'Engadget中国', 'IT之家', 'ZEALER', '数字尾巴', 'Chiphell', '苏宁数码', '京东数码', '开源中国', 'Segmentfault', 'v2ex',
          'CSDN', '博客园', '开发者头条', '掘金', '智联招聘', '拉勾网', 'BOSS直聘', '前程无忧', '猎聘网', '100offer', '内推网']

# @app.route("/index", methods=['GET', 'POST'], endpoint='root')  # 路由,请求方法为哪些
# def index():  # 视图函数
#     # title = 'Flask Web Dev'
#     print('----->', request.args.get('info'))  # 获取form提交的值。Post传递的参数 argus不能获取值
#     # print('-------->', request.form.get('info'))  # 获取form提交的值。Post传递的参数 argus不能获取值,只能使用request.form
#     if request.args.get('info') in p_name:
#         item = {p_name.index(request.args.get('info')): request.args.get('info')}  # 获取搜索结果并保存为字典形式
#         # return render_template('show.html', title=title, data=item)
#         return 'Search results: {}'.format(item)
#
#     return render_template('index.html', data=p_name)
#
#
# @app.route('/user/<username>', endpoint='un')  # 一种标记
# def show_user_profile(username):
#     # show the user profile for that user
#     if username == 'admin':
#         return 'User %s' % escape(username)
#     return redirect(url_for('root'))  # 重定向
#
#
# def replace_hello(value):
#     # print("----->", value)
#     value = value.replace('城', '')
#     # print("----->", value)
#     return value.strip()
#
#
# app.add_template_filter(replace_hello, 'replace')  # 自定义函数
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     print(request.form.get('user'))
#     user = request.form.get('user')
#     if user == 'admin':
#         return '<br>System Reservation</br>'
#     return render_template('register.html')


if __name__ == "__main__":
    # app.run()
    manager.run()
