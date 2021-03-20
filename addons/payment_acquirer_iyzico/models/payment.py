from harpiya.exceptions import ValidationError, UserError
from harpiya.addons.payment_acquirer_iyzico.controllers.main import PaymentIyzicoController
from harpiya.tools.float_utils import float_compare, float_repr
from harpiya import models, fields, api, _
from werkzeug import urls
import pprint
import ast
import logging
_logger = logging.getLogger(__name__)
try:
    import iyzipay
except Exception as e:
    _logger.error("#BRQDEBUG-1 iyzipay-python library not installed.")


class PaymentIyzico(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('iyzico', 'Iyzico')])
    iyzico_api_key = fields.Char(
        string="Iyzico API Anahtarı", required_if_provider="iyzico", groups='base.group_user')
    iyzico_secret_key = fields.Char(
        string="Iyzico Güvenlik Anahtarı", required_if_provider="iyzico", groups='base.group_user')
    iyzico_api_url = fields.Char(
        string="Iyzico API URL", groups='base.group_user')

    def _get_option_dict(self) -> dict:
        option_dict = {
            'api_key': self.iyzico_api_key,
            'secret_key': self.iyzico_secret_key,
            'base_url': self.iyzico_api_url or iyzipay.base_url
        }
        return option_dict

    def _get_buyer_address(self, iyzico_txn_values: dict) -> dict:
        buyer_data = {
            'id': iyzico_txn_values.get('reference').split('-')[0],
            'name': iyzico_txn_values.get('billing_partner_first_name'),
            'surname': iyzico_txn_values.get('billing_partner_last_name'),
            'gsmNumber': iyzico_txn_values.get('billing_partner_phone'),
            'email': iyzico_txn_values.get('billing_partner_email'),
            'identityNumber': iyzico_txn_values.get('reference').split('-')[0],
            'registrationAddress': iyzico_txn_values.get('billing_partner_address'),
            'city': iyzico_txn_values.get('billing_partner_city'),
            'country': iyzico_txn_values.get('billing_partner_country').name,
            'zipCode': iyzico_txn_values.get('billing_partner_zip'),
        }
        return buyer_data

    def _get_shipping_address(self, iyzico_txn_values: dict) -> dict:
        shipping_data = {
            'contactName': iyzico_txn_values.get('partner_name'),
            'address': iyzico_txn_values.get('partner_address'),
            'city': iyzico_txn_values.get('partner_city'),
            'country': iyzico_txn_values.get('partner_country').name,
            'zipCode': iyzico_txn_values.get('partner_zip'),
        }
        return shipping_data

    def _get_billing_address(self, iyzico_txn_values: dict) -> dict:
        billing_data = {
            'contactName': iyzico_txn_values.get('billing_partner_name'),
            'address': iyzico_txn_values.get('billing_partner_address'),
            'city': iyzico_txn_values.get('billing_partner_city'),
            'country': iyzico_txn_values.get('billing_partner_country').name,
            'zipCode': iyzico_txn_values.get('billing_partner_zip'),
        }
        return billing_data

    def _get_basket_elements(self, iyzico_txn_values: dict) -> dict:
        basket_elements_list = []
        basket_elements = {
            'id': iyzico_txn_values.get('reference').split('-')[0],
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': float_repr(iyzico_txn_values.get('amount'), 2),
        }
        basket_elements_list.append(basket_elements)
        return basket_elements_list

    def _get_request_dict(self, iyzico_txn_values: dict) -> dict:
        base_url = self.get_base_url()
        iyzico_callback_url = urls.url_join(base_url, PaymentIyzicoController._iyzico_callback_url)
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        request_dict = {
            'locale': self._context.get('lang').split('_')[0],
            'price': float_repr(iyzico_txn_values.get('amount'), 2),
            'paidPrice': float_repr(iyzico_txn_values.get('amount'), 2),
            'currency': iyzico_txn_values.get('currency').name,
            'basketId': iyzico_txn_values.get('reference'),
            'paymentGroup': 'PRODUCT',
            "callbackUrl": urls.url_join(base_url, iyzico_callback_url),
            'buyer': self._get_buyer_address(iyzico_txn_values),
            'shippingAddress': self._get_shipping_address(iyzico_txn_values),
            'billingAddress': self._get_billing_address(iyzico_txn_values),
            'basketItems': self._get_basket_elements(iyzico_txn_values),
        }
        return request_dict

    def _get_response_elements(self, response_data: dict) -> dict:
        response = dict()
        response['status'] = response_data.get('status')
        response['errorCode'] = response_data.get('errorCode')
        response['errorMessage'] = response_data.get('errorMessage')
        response['paymentPageUrl'] = response_data.get('paymentPageUrl')
        response['token'] = response_data.get('token')
        return response

    def _get_response_data(self, iyzico_txn_values: dict) -> dict:
        try:
            checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(
                self._get_request_dict(iyzico_txn_values), self._get_option_dict())
            response = self._get_response_elements(ast.literal_eval(
                checkout_form_initialize.read().decode('utf-8')))
        except Exception as e:
            raise UserError(e)
        return response

    def get_retrive_data(self, data: dict) -> dict:
        try:
            data.update({'locale': self._context.get('lang').split('_')[0]})
            checkout_form_retrieve = iyzipay.CheckoutForm()
            retrieve_data = checkout_form_retrieve.retrieve(
                data, self._get_option_dict())
            response = ast.literal_eval(retrieve_data.read().decode('utf-8'))
        except Exception as e:
            raise UserError(e)
        return response

    def iyzico_form_generate_values(self, values):
        iyzico_txn_values = dict(values)
        response_data = self._get_response_data(iyzico_txn_values)
        iyzico_txn_values.update(response_data)
        return iyzico_txn_values

    @api.model
    def _create_missing_journal_for_acquirers(self, company=None):
        acquirer_modules = self.env['ir.module.module'].search(
            [('name', 'like', 'payment_%'), ('state', 'in', ('to install', 'installed'))])
        acquirer_names = [a.name.split('_')[-1] for a in acquirer_modules]

        company = company or self.env.company
        acquirers = self.env['payment.acquirer'].search(
            [('provider', 'in', acquirer_names), ('journal_id', '=', False), ('company_id', '=', company.id)])

        journals = self.env['account.journal']
        for acquirer in acquirers.filtered(lambda l: not l.journal_id and l.company_id.chart_template_id):
            acquirer.journal_id = self.env['account.journal'].create(
                acquirer._prepare_account_journal_vals())
            journals += acquirer.journal_id
        return journals


class TrasanctionIyzicoPayment(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _iyzico_form_get_tx_from_data(self, data):
        reference, amount, currency, payment_id, auth_code = data.get('basketId'), data.get(
            'price'), data.get('currency'), data.get('paymentId'), data.get('authCode'),
        if not (reference and amount and currency and payment_id and auth_code):
            raise ValidationError(_("Required data missing from response."))

        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = _('received data for reference %s') % (
                pprint.pformat(reference))
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def _iyzico_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if float_compare(float(data.get('price', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('amount', data.get('price'), '%.2f' % self.amount))
        if data.get('currency') != self.currency_id.name:
            invalid_parameters.append(
                ('currency', data.get('currency'), self.currency_id.name))
        return invalid_parameters

    def _iyzico_form_validate(self, data):
        status = data.get('status')
        res = {
            'date': fields.datetime.now(),
            'acquirer_reference': data.get('paymentId'),
            'state_message': status
        }
        self.write(res)
        if status == "success":
            self._set_transaction_done()
            self.execute_callback()
            _logger.info(
                'Validated Iyzico payment for tx %s: set as done' % (self.reference))
            return True
        else:
            error = data.get('errorMessage')
            _logger.error(error)
            self._set_transaction_error(error)
            return False
