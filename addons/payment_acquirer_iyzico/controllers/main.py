import logging
import pprint
import werkzeug

from harpiya import http
from harpiya.http import request

_logger = logging.getLogger(__name__)


class PaymentIyzicoController(http.Controller):
    _iyzico_callback_url = '/payment/iyzico/callback'

    @http.route([_iyzico_callback_url], type='http', auth='public', csrf=False)
    def lloyds_checkout_success(self, **kwargs):
        token = kwargs.get('token')
        _logger.info('Iyzico Payment Connect: entering form_feedback with post data %s' % pprint.pformat(kwargs))
        data = {'token': token}
        if token:
            acquirer_obj = request.env['payment.acquirer'].sudo().search([('provider', '=', 'iyzico')])
            res = acquirer_obj.get_retrive_data(data)
            data.update(res)
        request.env['payment.transaction'].sudo().form_feedback(data, 'iyzico')
        return werkzeug.utils.redirect('/payment/process')
