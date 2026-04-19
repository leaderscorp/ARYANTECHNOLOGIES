# Copyright 2020 Alexandre Díaz <dev@redneboa.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Odoo 19 migration notes:
#   - _generate_asset_links_cache removed in v19; only _generate_asset_links remains.
#   - _get_asset_nodes() gained an 'autoprefix' kwarg in v19.
#   - We use **kwargs to future-proof all signatures.
import logging

from odoo import models

from .assetsbundle import AssetsBundleCompanyColor

_logger = logging.getLogger(__name__)

_BUNDLE = "web_company_color.company_color_assets"
_CUSTOM_SCSS_PREFIX = "/web_company_color/static/src/scss/custom_colors."


class QWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    # ------------------------------------------------------------------
    # v18 cache variant (kept for backward compat, harmless on v19)
    # ------------------------------------------------------------------
    def _generate_asset_links_cache(self, bundle, css=True, js=True,
                                     assets_params=None, rtl=False, **kwargs):
        res = super()._generate_asset_links_cache(
            bundle, css=css, js=js, assets_params=assets_params, rtl=rtl, **kwargs
        )
        if bundle == _BUNDLE:
            asset = AssetsBundleCompanyColor(bundle, [], env=self.env)
            res += [asset.get_company_color_asset_node()]
        return res

    # ------------------------------------------------------------------
    # v19 main variant
    # ------------------------------------------------------------------
    def _generate_asset_links(self, bundle, css=True, js=True,
                               debug_assets=False, assets_params=None,
                               rtl=False, **kwargs):
        res = super()._generate_asset_links(
            bundle, css=css, js=js, debug_assets=debug_assets,
            assets_params=assets_params, rtl=rtl, **kwargs
        )
        if bundle == _BUNDLE:
            asset = AssetsBundleCompanyColor(bundle, [], env=self.env)
            res += [asset.get_company_color_asset_node()]
        return res

    def _get_asset_content(self, bundle, assets_params=None, **kwargs):
        """Handle 'special' web_company_color bundle."""
        if bundle == _BUNDLE:
            return [], []
        return super()._get_asset_content(bundle, assets_params=assets_params, **kwargs)

    # ------------------------------------------------------------------
    # Accept any extra kwargs Odoo 19 may pass (e.g. autoprefix)
    # ------------------------------------------------------------------
    def _get_asset_nodes(self, bundle, css=True, js=True, debug=False,
                          defer_load=False, lazy_load=False, media=None,
                          **kwargs):
        res = super()._get_asset_nodes(
            bundle, css=css, js=js, debug=debug,
            defer_load=defer_load, lazy_load=lazy_load, media=media,
            **kwargs
        )
        for tag, attributes in res:
            if tag == "link" and attributes.get("href", "").startswith(
                _CUSTOM_SCSS_PREFIX
            ):
                attributes.pop("type", None)
        return res
