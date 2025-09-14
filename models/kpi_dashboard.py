from odoo import models, fields, api


class KpiDashboard(models.Model):
    _name = 'kpi.dashboard'
    _description = 'KPI Dashboard'

    name = fields.Char(string='Nombre', required=True, default='Dashboard Principal')

    total_projects = fields.Integer(compute='_compute_stats')
    active_projects = fields.Integer(compute='_compute_stats')
    completed_projects = fields.Integer(compute='_compute_stats')
    total_tasks = fields.Integer(compute='_compute_stats')
    completed_tasks = fields.Integer(compute='_compute_stats')
    overdue_tasks = fields.Integer(compute='_compute_stats')

    @api.depends('name')
    def _compute_stats(self):
        for dashboard in self:
            projects = self.env['kpi.project'].search([])
            tasks = self.env['kpi.task'].search([])

            dashboard.total_projects = len(projects)
            dashboard.active_projects = len(projects.filtered(lambda p: p.state == 'in_progress'))
            dashboard.completed_projects = len(projects.filtered(lambda p: p.state == 'completed'))
            dashboard.total_tasks = len(tasks)
            dashboard.completed_tasks = len(tasks.filtered(lambda t: t.state == 'completed'))
            dashboard.overdue_tasks = len(tasks.filtered(lambda t: t.state == 'delayed'))