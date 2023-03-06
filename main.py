from pycqBot.cqApi import cqHttpApi, cqLog
import logging
import cf
from pycqBot import Message
from cf import CFSpider
import secret_tokens

cqLog(logging.DEBUG)
cqapi = cqHttpApi()

def cf1(commandData, message: Message):
    HOURS = 200
    cfs = CFSpider()
    contest_list = cfs.get_recent_contest(countdown_limit_hours=HOURS)
    if len(contest_list) == 0:
        message.reply(f'近 {HOURS} 小时内无 Codeforces 竞赛')
    else:
        c = contest_list[0]
        msg = ''
        msg += f'- 竞赛名：{c.name}\n'
        msg += f'- 开始时间：{c.start_time}\n'
        msg += f'- 时长：{c.length}\n'
        msg += f'- 倒计时：{c.countdown()}\n'
        message.reply(msg)

def cf_autofetch(from_id):
    HOURS = 80
    cfs = CFSpider()
    contest_list = cfs.get_recent_contest(3, countdown_limit_hours=HOURS)
    print(f'got {contest_list}')
    if len(contest_list) > 0:
        msg = '近期的（目前在测试 80 小时内的）Codeforces 竞赛提醒：'
        for c in contest_list:
            msg += f'\n- 竞赛名：{c.name}\n'
            msg += f'- 开始时间：{c.start_time}\n'
            msg += f'- 时长：{c.length}\n'
            msg += f'- 倒计时：{c.countdown()}\n'
        cqapi.send_group_msg(from_id, msg)

bot = cqapi.create_bot(
    group_id_list = secret_tokens.GROUP_ID_LIST,
    options = secret_tokens.OPTIONS,
)

bot.command(cf1, "cf1", {
    "help": [
        "#cf1 - 获取最近一场 Codeforces 竞赛信息"
    ]
}).timing(cf_autofetch, "cf-autofetch", {
    "timeSleep": 28800
})

bot.start()