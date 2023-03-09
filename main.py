from pycqBot.cqApi import cqHttpApi, cqLog
import logging
import cf
from pycqBot import Message
from cf import CFSpider, CFContest
import secret_tokens
import ratings
import leetcode

cqLog(logging.DEBUG)
cqapi = cqHttpApi()

def cf_contest_info_str(c: CFContest) -> str:
    msg = ''
    msg += f'- 竞赛名：{c.name}\n'
    msg += f'- 开始时间：{c.start_time_as_str()}\n'
    msg += f'- 时长：{c.length}\n'
    msg += f'- 倒计时：{c.countdown_as_str()}\n'
    msg += f'- 链接：{c.url}\n'
    return msg

def cf1(commandData, message: Message):
    HOURS = 72
    cfs = CFSpider()
    contest_list = cfs.get_recent_contest(countdown_limit_hours=HOURS)
    if len(contest_list) == 0:
        message.reply(f'近 {HOURS} 小时内无 Codeforces 竞赛')
    else:
        c = contest_list[0]
        msg = cf_contest_info_str(c)
        message.reply(msg)

def cf(commandData, message: Message):
    HOURS = 72
    cfs = CFSpider()
    contest_list = cfs.get_recent_contest(5, countdown_limit_hours=HOURS)
    if len(contest_list) == 0:
        message.reply(f'近 {HOURS} 小时内无 Codeforces 竞赛')
    else:
        msg = ''
        for c in contest_list:
            msg += cf_contest_info_str(c)
            msg += '\n'
        message.reply(str.rstrip(msg))

def cf_autofetch(from_id):
    HOURS = 33
    cfs = CFSpider()
    contest_list = cfs.get_recent_contest(3, countdown_limit_hours=HOURS)
    print(f'got {contest_list}')
    if len(contest_list) > 0:
        msg = '近期的 Codeforces 竞赛提醒：'
        for c in contest_list:
            msg += '\n'
            msg += cf_contest_info_str(c)
        cqapi.send_group_msg(from_id, msg)

def rat_cf(command, message: Message):
    kvs = ratings.get_cf_ratings()
    if len(kvs) == 0 and len(secret_tokens.RATING_LIST) == 0:
        message.reply('rating list 为空')
    elif len(kvs) == 0:
        message.reply('爬虫炸了')
    else:
        msg = 'Codeforces Ratings:\n'
        for name, rating in kvs:
            msg += f'{name}: {rating}\n'
        message.reply(msg)

def lc(command, message: Message):
    lc_problem = leetcode.get_daily_url()
    msg = \
f'''\
力扣 CN 每日一题：
{lc_problem.no} - {lc_problem.title}
难度：{lc_problem.level}
链接：{lc_problem.url}
'''
    message.reply(str.strip(msg))

def include(command, message: Message):
    message.reply('代码写得不错！')

bot = cqapi.create_bot(
    group_id_list = secret_tokens.GROUP_ID_LIST,
    options = secret_tokens.OPTIONS,
)

bot.command(cf1, "cf1", {
    "help": [
        "#cf1 - 获取最近一场 Codeforces 竞赛信息"
    ]
}).command(cf, "cf", {
    "help": [
        "#cf - 获取最近多场 Codeforces 竞赛信息"
    ]
}).timing(cf_autofetch, "cf-autofetch", {
    "timeSleep": 28800
}).command(rat_cf, "rat-cf", {
    "help": [
        "#rat-cf - 获取指定用户的 Codeforces contest rating"
    ]
}).command(lc, "lc", {
    "help": [
        "#lc - 获取力扣 CN 每日一题"
    ]
}).command(include, "include")

bot.start()
