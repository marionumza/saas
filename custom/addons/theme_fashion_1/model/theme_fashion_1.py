from harpiya import models

class theme_utils(models.AbstractModel):
    _inherit = 'theme.utils'
    
    
    def _theme_fashion_1_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
