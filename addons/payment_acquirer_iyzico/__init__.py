from . import controllers
from . import models
from harpiya.addons.payment.models.payment_acquirer import create_missing_journal_for_acquirers

def pre_init_check(cr):
    from harpiya.service import common
    from harpiya.exceptions import Warning
    version_info = common.exp_version()
    server_series = version_info.get('server_serie')
    if server_series != '13.0':
        raise Warning('Module support Harpiya series 13.0 found {}'.format(server_series))
    return True
