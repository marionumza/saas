harpiya.define('iap.redirect_harpiya_credit_widget', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');


var IapHarpiyaCreditRedirect = AbstractAction.extend({
    template: 'iap.redirect_to_harpiya_credit',
    events : {
        "click .redirect_confirm" : "harpiya_redirect",
    },
    init: function (parent, action) {
        this._super(parent, action);
        this.url = action.params.url;
    },

    harpiya_redirect: function () {
        window.open(this.url, '_blank');
        this.do_action({type: 'ir.actions.act_window_close'});
        // framework.redirect(this.url);
    },

});
core.action_registry.add('iap_harpiya_credit_redirect', IapHarpiyaCreditRedirect);
});
