from odoo import models, api, fields, _, http
from odoo.exceptions import Warning, UserError
import logging

_logger = logging.getLogger(__name__)

class ResPartnerCounty(models.Model):
    _name = 'res.partner.county'
    _description = 'County'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("County Name", required=True)
    sub_county = fields.Many2one("res.partner.subcounty")

class ResPartnerSubCounty(models.Model):
    _name = 'res.partner.subcounty'
    _description = 'Subcounty'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Sub-County Name",required=True)
    ward = fields.Many2one("res.partner.ward")
    subcounty = fields.Many2one("res.partner.county", string="County")

class ResPartnerWard(models.Model):
    _name = 'res.partner.ward'
    _description = 'Ward'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Ward Name",required=True)
    subcounty = fields.Many2one("res.partner.county", string="County")


