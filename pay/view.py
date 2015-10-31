# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import time

import types
import wxpay
import random
import logging

from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.qfresponse import *
from qfcommon.base.dbpool import with_database
from lib.smuser import with_customer_weixin, with_customer


import config

log = logging.getLogger()


class Wap(core.Handler):

    def get_req_param(self):
        '''获取参数'''

        out_sn = ''.join(random.sample('0123456789', 8))
        input = {'out_sn': out_sn, 'total_amt': '1', 'address': '望京融科', 'goods_name': '支付测试'}
        #data['token'] = input.get('token','').strip()
        #data['code'] = input.get('code','').strip()
        #data['openid'] = input.get('openid','').strip()
        #data['order_token'] = input.get('order_token','').strip()

        data['out_sn'] = input.get('out_sn','').strip()
        data['total_amt'] = input.get('total_amt','').strip()
        data['address'] = input.get('address','').strip().decode('utf-8')
        data['mobile'] = input.get('mobile','').strip()
        data['goods_name'] = input.get('goods_name','').strip()
        if type(data['goods_name']) == types.StringType:
            data['goods_name'] = data['goods_name'].decode('utf-8')
            data['goods_info'] = input.get('goods_info','').strip()
        if type(data['goods_info']) == types.StringType:
            data['goods_info'] = data['goods_info'].decode('utf-8')
            data['mchnt_name'] = input.get('mchnt_name','').strip()
        if type(data['mchnt_name']) == types.StringType:
            data['mchnt_name'] = data['mchnt_name'].decode('utf-8')
            data['pay_seq'] = input.get('pay_seq','')

        self.data = data

    @with_database('qf_wemall')
    def GET(self, args=""):
        """加载指定页面
        """
        self.get_req_param()
        pay_settings = {'pay_seq':[2,5]}
        self.write(template.render('pay/order.html', pay_settings=pay_settings, **self.data))


class PrePay(core.Handler):
    """微信预下单获取
    """
    def get_rep_parsm(self):
        params = {}
        input = self.req.input()

    @with_database('qf_wemall')
    def POST(self,args=""):

        self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})

        input = self.req.input()
        merid = input.get('merid')
        
        ret_val = {}
        if int(input['pay_type']) == 2:
            resp = wxpay.WxPayConf_pub.config(self.db, merid)
            if not resp:
                self.write(error(QFRET.NODATA, escape=False))
                log.info('respcd=%s|path=%s' % (QFRET.NODATA, self.req.path))
                return

            openid = input.get('openid')
            unified_order = wxpay.UnifiedOrder_pub()
            unified_order.setParameter('body',input['goods_name'])
            #unified_order.setParameter('out_trade_no',input['out_trade_no'])
            unified_order.setParameter('out_trade_no',input['out_sn'])
            unified_order.setParameter('total_fee',input['total_amt'])
            unified_order.setParameter('notify_url', '{0}{1}'.format(self.req.host, wxpay.WxPayConf_pub.NOTIFY_URL))
            unified_order.setParameter('openid', openid)
            unified_order.setParameter('trade_type','JSAPI')
            prepay_id = unified_order.getPrepayId()
            log.info('prepay_id=%s' % prepay_id)

            jsapi = wxpay.JsApi_pub()
            jsapi.setPrepayId(prepay_id)
            ret_val = jsapi.getParameters()
            log.info('ret_val=%s' % ret_val)

        self.write(success(ret_val, escape=False))

class CallBack(core.Handler):
    @with_database('qf_wemall')
    def GET(elf,args=""):
        """兼容微信支付宝钱台的回调 我方需正确处理对方重复回调
        """
        return
