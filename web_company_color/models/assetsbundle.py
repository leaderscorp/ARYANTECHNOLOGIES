# Copyright 2020 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Odoo 19 migration notes:
#   AssetsBundle was refactored/removed in Odoo 17+ in favour of ir.asset.
#   We keep this helper class but derive it from object instead of AssetsBundle
#   so the module doesn't break if AssetsBundle is no longer importable.
#   The only used method is get_company_color_asset_node(), which remains intact.
import logging

from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.base.models.assetsbundle import AssetsBundle as _Base
except ImportError:
    _Base = object


class AssetsBundleCompanyColor(_Base):
    def __init__(self, name, files, env=None, css=True, js=True):
        if _Base is not object:
            super().__init__(name, files, env=env, css=css, js=js)
        else:
            # Minimal stub when AssetsBundle no longer exists
            self.name = name
            self.env = env

    def get_company_color_asset_node(self):
        """Return the CSS URL for the active company's custom colors."""
        try:
            active_company_id = int(
                request.httprequest.cookies.get("cids", "").split("-")[0]
            )
        except Exception:
            active_company_id = False
        company_id = (
            self.env["res.company"].browse(active_company_id) or self.env.company
        )
        return company_id.scss_get_url()
