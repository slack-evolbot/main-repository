# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import random
import sys
import time

from slacker import Slacker
from slackbot_settings import API_TOKEN

slacker = Slacker(API_TOKEN)

ENEMY = '\nENEMY:'
ENEMY_HP =  200
ENEMY_POWER =  30

LINE = '\n-----------------------------------'

ME = '\nYOU     :'
ME_HP = 200
ME_POWER =  40

COMMAND = '\n①戦う\n②逃げる'

class resp(object):
    ts = 0
    mode = 0
    enemy_hp = ENEMY_HP
    me_hp = ME_HP

@listen_to(u'(冒険する)')
@respond_to(u'(冒険する)')
def resp_aplha(message, *something):
    if(resp.mode==0):
        re_message = slacker.chat.post_message(message.body['channel'],
                                               '敵が現れた' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + COMMAND,
                                               as_user=True
                                               )
        resp.ts = re_message.body['ts']
        resp.mode = 1

    else:
        slacker.chat.update(message.body['channel'],
                            resp.ts,
                            '敵が現れた' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + COMMAND
                            )
        resp.mode = 1
        
    
@listen_to(u'(1|１|①|戦う)')
@respond_to(u'(1|１|①|戦う)')    
def resp_battle(message, *something):
    if(resp.mode==1):
        damage = random.randint(ME_POWER * 0.7,ME_POWER)
        resp.enemy_hp -= damage

        if resp.enemy_hp > 0:
            slacker.chat.update(message.body['channel'],
                                resp.ts,
                                '敵に' + str(damage) + 'のダメージ' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + '敵のターン'
                                )
            time.sleep(5)
            damage = random.randint(ENEMY_POWER * 0.7,ENEMY_POWER)
            resp.me_hp -= damage
            
            if resp.me_hp > 0:
                slacker.chat.update(message.body['channel'],
                                resp.ts,
                                str(damage) + 'のダメージをうけた' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + COMMAND
                                )
            else:
                slacker.chat.update(message.body['channel'],
                                    resp.ts,
                                    '目の前が真っ暗になった' + ENEMY + hit_point(ENEMY_HP, 0) + ME + hit_point(ENEMY_HP, resp.me_hp) 
                                    )
        else:
            slacker.chat.update(message.body['channel'],
                                resp.ts,
                                'やった敵を倒したぞ' + ENEMY + hit_point(ENEMY_HP, 0) + ME + hit_point(ENEMY_HP, resp.me_hp) 
                                )
            resp.mode = 0
    else:
        re_message = slacker.chat.post_message(message.body['channel'],
                                               'お主はまだ冒険に出ておらぬぞ',
                                               as_user=True
                                               )
        resp.ts = re_message.body['ts']
        resp.mode = 2

@listen_to(u'(2|２|②|逃げる)')
@respond_to(u'(2|２|②|逃げる)')
def resp_escape(message, *something):
    if(resp.mode==1):
        re_message = slacker.chat.update(message.body['channel'],
                                         resp.ts,
                                         'だめだ逃げられない' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + COMMAND
                                        )
    else:
        re_message = slacker.chat.post_message(message.body['channel'],
                                                'お主はまだ冒険に出ておらぬぞ',
                                                as_user=True
                                                )
        resp.ts = re_message.body['ts']
        resp.mode = 2
        
@listen_to(u'(^(?!(1|１|①|冒険する|2|２|②|戦う)).+$)')
@respond_to(u'(^(?!(1|１|①|冒険する|2|２|②|戦う)).+$)')
def resp_noaction(message, *something):    
    if(resp.mode==1):
        re_message = slacker.chat.update(message.body['channel'],
                                 resp.ts,
                                 '君はそんなことできないぞ' + ENEMY + hit_point(ENEMY_HP, resp.enemy_hp) + ME + hit_point(ENEMY_HP, resp.me_hp) + COMMAND
                                )
    else:
        re_message = slacker.chat.post_message(message.body['channel'],
                                               'お主はまだ冒険に出ておらぬぞ',
                                               as_user=True
                                               )
        resp.ts = re_message.body['ts']
        resp.mode = 2

def hit_point(max_hp, now_hp):
    return '[' + ('|' * int(float(now_hp/max_hp) * 30)) + (' ' * int(((max_hp-now_hp)/max_hp) * 30)) + ']\n' 
