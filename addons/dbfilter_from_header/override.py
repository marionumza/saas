import logging
import re

from harpiya import http
from harpiya.tools import config

db_filter_org = http.db_filter


def db_filter(dbs, httprequest=None):
    dbs = db_filter_org(dbs, httprequest)
    httprequest = httprequest or http.request.httprequest
    db_filter_hdr = httprequest.environ.get("HTTP_X_HARPIYA_DBFILTER")
    if db_filter_hdr:
        dbs = [db for db in dbs if re.match(db_filter_hdr, db)]
    return dbs


if config.get("proxy_mode") and "dbfilter_from_header" in config.get(
    "server_wide_modules"
):
    _logger = logging.getLogger(__name__)
    _logger.info("monkey patching http.db_filter")
    http.db_filter = db_filter