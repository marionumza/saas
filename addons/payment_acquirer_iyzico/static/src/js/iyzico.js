harpiya.define('payment_acquirer_iyzico.payment_acquirer_iyzico', function(require){
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    var qweb = core.qweb;
    var _t = core._t;

    if ($.blockUI) {
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }

    var IyzicoPaymentForm = publicWidget.Widget.extend({
        init: function(){
            this.$form = $('form[provider="iyzico"]');
            this.formData = {};
            this.start();  
        },
        start: function(){
            var self = this;
            self._initializeIyzicoPayment();
        },
        _initializeIyzicoPayment: function(){
            this._initBlockUI(_t("Kredi kartı ile ödeme başlatılıyor..."));
            var self = this;
            this.formData = self._getFormData();
            console.log(this.formData)
            if(this.formData.status == "success"){
                self._redirectToPayment();
            }else{
                self._showErrorMessage(_t('Iyzico Hatası'), this.formData.errorMessage);
            }
        },
        _getFormData: function() {
            var data = {}
            this.$form.find('input').each(function() {
                data[$(this).attr('name')] = $(this).val();
            });
            return data
        },
        _redirectToPayment: function(){
            this._initBlockUI(_t("Kredi kartı ödemeye yönlendiriliyor.."));
            window.open(this.formData.paymentPageUrl, "_self")
        },
        _showErrorMessage: function(title, message) {
            this._revokeBlockUI();
            $("#o_payment_form_pay").hide();
            return new Dialog(null, {
                title: _t('Error: ') + _.str.escapeHTML(title),
                size: 'medium',
                $content: "<p>" + (_.str.escapeHTML(message) || "") + "</p>" ,
                buttons: [
                {text: _t('Ok'), close: true}]}).open();
        },
        _initBlockUI: function(message) {
            if ($.blockUI) {
                $.blockUI({
                    'message': '<h2 class="text-white"><img src="/web/static/src/img/spin.png" class="fa-pulse"/>' +
                            '    <br />' + message +
                            '</h2>'
                });
            }
            $("#o_payment_form_pay").attr('disabled', 'disabled');
        },
        _revokeBlockUI: function() {
            if ($.blockUI) {
                $.unblockUI();
            }
            $("#o_payment_form_pay").removeAttr('disabled');
        },
    });

    new IyzicoPaymentForm();
});