import logging
from odoo import models
from odoo.http import request


_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):

    _inherit = "ir.http"

    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    def session_info(self):
        try:
            result = super(IrHttp, self).session_info()
            result['chatter_position'] = self.env.user.chatter_position
            return result
        except ValueError as e:
            _logger.warning(e)
            return _('Not session info')
