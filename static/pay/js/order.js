$(function(){
    function init(){
        $($('input[name=pay_type]')[0]).attr('checked','checked')
        get_amt()
    }
    init();

    function check_weixin_useragent(){
        return navigator.userAgent.indexOf('MicroMessenger') != -1;
    }

    function get_amt(){
        if($('#id-coupon').length > 0){
            pay_amt = order_amt - coupon_map[$('#id-coupon').val()];
        }
        if($('#id-balance').length > 0){
            if($('#id-balance').is(':checked')){
                if(balance_amt >= pay_amt){
                    balance_use = pay_amt;
                    pay_amt = 0;
                }else{
                    balance_use = balance_amt;
                    pay_amt = pay_amt - balance_amt;
                }
            }else{
                balance_use = 0;
            }
        }
        $('#id-pay-amt').html(pay_amt / 100.0);

    }
    $('#id-coupon').change(get_amt);
    $('#id-balance').change(get_amt);
    $('#id-submit').click(function(){
        $(this).attr('disabled', 'disabled');
        par_pay_type = $('input[name=pay_type]:checked').val();
        if(par_pay_type === undefined && pay_amt > 0){
            alert('请选择合适的支付方式')
            $(this).attr('disabled',null);
            return
        }
        if(par_pay_type == 1 && check_weixin_useragent()){
            $('.mask').css('display','block');
            $(this).attr('disabled',null);
            return
        }
        par_app_code = $('#id-app_code').val();
        par_out_sn = $('#id-out_sn').val();
        par_order_token = $('#id-order_token').val();
        par_goods_name = $('#id-goods_name').val();
        par_openid = $('#id-openid').val();
        $.ajax({
            type : 'POST',
            url : '/pay/prepay',
            data : {
                total_amt : order_amt,
                pay_amt : pay_amt,
                pay_type : par_pay_type,
                out_sn : par_out_sn,
                goods_name : par_goods_name,
            },
            success : function(data) {
                data = JSON.parse(data);
                if(data.respcd === "0000"){
                    //如果需要支付
                    if(pay_amt > 0){
                        if(par_pay_type == 4){
                            if(data['data']['url'] == ''){
                                alert('支付宝参数错误');
                            }else{
                                window.location.href=data['data']['url'];
                            }
                            $('#id-submit').attr('disabled',null);
                        }else if(par_pay_type == 6){
			    
                            if(data['data'] == '{}'){
                                alert('微信支付参数错误');
                                $('#id-submit').attr('disabled',null);
                            }else{
                                WeixinJSBridge.invoke('getBrandWCPayRequest', JSON.parse(data['data']),function(res){
                                    if(res.err_msg == "get_brand_wcpay_request:ok"){
                                        //window.location.href='/m/view?t=wm&p=orderdetail&order_sn=' + par_out_sn + '&merid=' + merid + '&shopkey=' + shopkey + '&name=' + name + '&subname=' + subname;
                                        window.location.href='/m/3e5471cd97e8f675d9ec8ba9d87fd103';
                                    }else if(res.err_msg == "get_brand_wcpay_request:cancel") {
                                    }else{
                                        alert('微信系统繁忙');
                                    }
                                    $('#id-submit').attr('disabled',null);
                                });
                            }
                        }else{
                            window.location.href='/v1/wap/callback/normal?orderid='+data['data']['order_id'];
                        }
                    }else{
                        window.location.href='/v1/wap/callback/normal?orderid='+data['data']['order_id'];
                    }
                }else{
                    alert(data['respmsg']);
                    $('#id-submit').attr('disabled',null);
                }
            }

        })
    })
    $('.mask-btn').click(function(){
        $('.mask').css('display','none');
    })

});

