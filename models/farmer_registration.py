from odoo import models, api, fields, _, http
from odoo.exceptions import Warning, UserError
import phonenumbers
import logging

_logger = logging.getLogger(__name__)

class FarmerRegistration(models.Model):
    _inherit = 'res.partner'
    country_id = fields.Many2one("res.country", string="Country",default=lambda self: self.env['res.country'].search(
        [('name', '=', 'Kenya')], limit=1),)
    reg_no = fields.Char("No#",readonly=True)
    id_number = fields.Char("ID Number")
    county = fields.Many2one("res.partner.county",string="County")
    wards = fields.Many2one("res.partner.ward", string="Ward")
    gps_location = fields.Char("Gps Location")
    partner_type = fields.Selection([('farmer','Farmer'),('agent','Agents'),('harvester','Harvesters'),('others','Others')], string="Type")
    notes = fields.Text("Notes")
    source = fields.Selection([('ussd', 'USSD'), ('app', 'App'), ('erp', 'ERP')])
    state = fields.Selection([('new','Awaiting Approval'),('approved','Approved'),('reject','Rejected')], default='new')
    responsible_id = fields.Many2one("hr.employee", default=lambda self: self.env['hr.employee'].search(
        [('user_id', '=', self.env.uid)], limit=1), )



    _sql_constraints = [
        ('phone', 'unique (phone)', 'The Farmer with this Phone Number already Exists!'),

    ]

    @api.model
    def create(self, vals):
        if vals['partner_type']=='farmer':
            name = self.env['ir.sequence'].next_by_code('farmer.engagement.seq')
            vals.update({
            'reg_no': name
        })
        res = super(FarmerRegistration, self).create(vals)
        return res

    @api.constrains('phone')
    def _check_phone(self):
        partner_rec = self.env['res.partner'].search(
            [('phone', '=', self.phone), ('id', '!=', self.id)])
        if partner_rec:
            raise UserError(_('Exists ! Already a Name exists with this Phone Number'))

    @api.constrains('id_number')
    def _check_id(self):
        partner_rec = self.env['res.partner'].search(
            [('id_number', '=', self.id_number), ('id', '!=', self.id)])
        if partner_rec:
            raise UserError(_('Exists ! Already a Name exists with this ID Number'))

    def action_approve(self):
        for rec in self:
            #update the Farmer Registration Number first 3 characters of Count+3xtors of Ward + n..
            if rec.reg_no:
                rec.reg_no=rec.county.name[0: 3]+(rec.reg_no).replace(rec.reg_no[0: 3], rec.wards.name[0:3])
            if not rec.responsible_id.work_email:
                raise UserError(_('Error ! Responsible: {} Must have work email'.format(rec.responsible_id.name)))
            #Try to send sms and email to update farmer of approval
            try:
                if phonenumbers.parse(rec.phone):
                    my_sms = self.env['sms.composer'].create(
                        {'numbers': rec.phone, 'body': "Record {} is approved by {}!".format(rec.name,rec.company_id.name)})
                    my_sms.action_send_sms()

                    rec.send_mail("Record {} has been approved-".format(rec.name), rec.responsible_id.name,
                          rec.responsible_id.work_email,
                          rec.responsible_id.name)
                    if rec.email:
                        rec.send_mail("Record {} has been Approved-".format(rec.name), rec.name,
                              rec.email,
                              rec.name)
                    rec.write({'state': 'approved'})
            except phonenumbers.NumberParseException:
                raise UserError(
                    _("The phone number entered:{} for {}  is not valid should start with +254......".format(
                        rec.phone, rec.name)))

    def reject(self):
        for rec in self:
            if not rec.responsible_id.work_email:
                raise UserError(_('Error ! Responsible: {} Must have work email'.format(rec.responsible_id.name)))

            rec.send_mail("Record {} has been rejected-".format(rec.name), rec.responsible_id.name,
                          rec.responsible_id.work_email,
                          rec.responsible_id.name)
            if rec.email:
                rec.send_mail("Record {} has been rejected-".format(rec.name), rec.name,
                              rec.email,
                              rec.name)
            rec.write({'state': 'reject'})

    def reject(self):
        for rec in self:
            rec.write({'state': 'new'})

    @api.onchange("state")
    def onchange_state(self):
        for rec in self:
            if self.env.user.has_group('farmer_engagement.group_farmer_engagement_manager'):
               rec.write({'state':'approved'})





    def send_mail(self, body_html, param, email_to, doc_name):
        mail_object = self.env['mail.mail'].create({
            'body_html': body_html + param + "  link :  " + "{}/web?db={}#id={}&view_type=form&model={}".format(
                self.env['ir.config_parameter'].sudo().get_param('web.base.url'), self._cr.dbname, self.id,
                'res.partner'),
            'email_to': email_to,
            'headers': 'Soko Fresh Farmer Engagement',
            'subject': 'Soko Fresh Farmer Engagement:' + doc_name,
        })

