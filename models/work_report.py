from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EmployeeWorkReport(models.Model):
    _name = 'employee.work.report'
    _description = 'Employee Work Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char('Reference', readonly=True,  copy=False, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,
        default=lambda self: self.env.user.employee_id.id)
    department_id = fields.Many2one('hr.department', string='Department',
        related='employee_id.department_id', store=True)
    manager_id = fields.Many2one('hr.employee', string='Manager',
        related='employee_id.parent_id', store=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    hours_worked = fields.Float('Hours Worked', required=True)
    work_summary = fields.Text('Work Summary', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.work.report') or 'New'
        return super(EmployeeWorkReport, self).create(vals_list)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    @api.constrains('hours_worked')
    def _check_hours_worked(self):
        for record in self:
            if record.hours_worked <= 0:
                raise ValidationError(_('Hours worked must be greater than zero.'))
            if record.hours_worked > 24:
                raise ValidationError(_('Hours worked cannot exceed 24 hours per day.'))

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_('You can only delete reports in draft state.'))
        return super(EmployeeWorkReport, self).unlink()

