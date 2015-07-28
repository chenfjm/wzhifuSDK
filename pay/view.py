# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import time
import tornado
import types
import wxpay

#import config

class Wap(tornado.web.RequestHandler):

    def get_req_param(self):
        '''获取参数'''

        data = {}
        #input = self.request.arguments
        input = {'out_sn': '1234567894', 'total_amt': '1', 'address': '望京融科', 'goods_name': '支付测试'}
        #data['token'] = input.get('token','').strip()
        #data['code'] = input.get('code','').strip()
        #data['openid'] = input.get('openid','').strip()
        data['openid'] = self.ses.get('openid', '0')
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

    def GET(self, args=""):
        """加载指定页面
        """
        self.get_req_param()
        pay_settings = {'pay_seq':[2,5]}
        self.render("templates/pay/order.html", pay_settings=pay_settings, **self.data)


class PrePay(tornado.web.RequestHandler):
    """微信预下单获取
    """

    def POST(self,args=""):

        #resp = wxpay.WxPayConf_pub.config(self.db, merid)
        #if not resp:
            #self.write(error(QFRET.NODATA, escape=False))
            #log.info('respcd=%s|path=%s|time=%0.3fms' % (QFRET.NODATA, self.req.path, (time.time() - start_time) * 1000))
            #return

        input = self.request.arguments
        merid = input.get('merid')
        openid = input.get('openid', '0')
        ret_val = {}
        if int(input['pay_type']) == PAY_TYPE_WXPAY_H5:
            unified_order = wxpay.UnifiedOrder_pub()
            unified_order.setParameter('body',input['goods_name'])
            #unified_order.setParameter('out_trade_no',input['out_trade_no'])
            unified_order.setParameter('out_trade_no',input['out_sn'])
            unified_order.setParameter('total_fee',input['total_amt'])
            unified_order.setParameter('notify_url', '{0}{1}'.format(self.req.host, wxpay.WxPayConf_pub.NOTIFY_URL))
            unified_order.setParameter('openid', openid)
            unified_order.setParameter('trade_type','JSAPI')
            prepay_id = unified_order.getPrepayId()

            jsapi = wxpay.JsApi_pub()
            jsapi.setPrepayId(prepay_id)
            ret_val = jsapi.getParameters()
        elif input['pay_type'] == PAY_TYPE_ALIPAY_H5:
            pass

        self.write(success(ret_val))

class CallBack(tornado.web.RequestHandler):
    def GET(elf,args=""):
        """兼容微信支付宝钱台的回调 我方需正确处理对方重复回调
        """
        return

def success(data, resperr='', debug=False, escape=True, encoder=None):
    ret = {"respcd": "0000", "resperr": resperr, "respmsg": "", "data": data}
    return simplejson.dumps(ret, ensure_ascii=escape, cls=encoder, separators=(',', ':'), default = json_default_trans)
