from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class KpiProject(models.Model):
    _name = 'kpi.project'
    _description = 'KPI Project - Professional Edition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Nombre del Proyecto', required=True, tracking=True)
    code = fields.Char(string='Código de Proyecto', required=True, tracking=True)
    description = fields.Text(string='Descripción')
    partner_id = fields.Many2one('res.partner', string='Cliente/Contacto')
    manager_id = fields.Many2one('res.users', string='Gerente de Proyecto', default=lambda self: self.env.user)

    start_date = fields.Date(string='Fecha de Inicio', default=fields.Date.today, tracking=True)
    end_date = fields.Date(string='Fecha de Finalización', tracking=True)
    actual_end_date = fields.Date(string='Fecha Real de Fin', readonly=True)

    budget = fields.Float(string='Presupuesto', digits=(16, 2))
    actual_cost = fields.Float(string='Costo Real', digits=(16, 2), compute='_compute_costs')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('on_hold', 'En Pausa'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)

    priority = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica')
    ], string='Prioridad', default='medium')

    completion_percentage = fields.Float(string='% Completado', digits=(5, 2), compute='_compute_metrics', store=True)
    health_status = fields.Selection([
        ('excellent', 'Excelente'),
        ('good', 'Bueno'),
        ('warning', 'Advertencia'),
        ('critical', 'Crítico')
    ], string='Estado de Salud', compute='_compute_metrics')

    task_ids = fields.One2many('kpi.task', 'project_id', string='Tareas')
    team_member_ids = fields.Many2many('res.users', string='Miembros del Equipo')

    total_tasks = fields.Integer(compute='_compute_metrics')
    completed_tasks = fields.Integer(compute='_compute_metrics')
    delayed_tasks = fields.Integer(compute='_compute_metrics')

    @api.depends('task_ids', 'task_ids.state')
    def _compute_metrics(self):
        for project in self:
            tasks = project.task_ids
            project.total_tasks = len(tasks)
            project.completed_tasks = len(tasks.filtered(lambda t: t.state == 'completed'))

            if project.total_tasks > 0:
                project.completion_percentage = (project.completed_tasks / project.total_tasks) * 100
            else:
                project.completion_percentage = 0.0

            if project.completion_percentage >= 90:
                project.health_status = 'excellent'
            elif project.completion_percentage >= 70:
                project.health_status = 'good'
            elif project.completion_percentage >= 50:
                project.health_status = 'warning'
            else:
                project.health_status = 'critical'

    def _compute_costs(self):
        for project in self:
            project.actual_cost = sum(project.task_ids.mapped('cost')) if project.task_ids else 0

    def action_start_project(self):
        self.write({'state': 'in_progress'})
        return True

    def action_complete_project(self):
        self.write({
            'state': 'completed',
            'actual_end_date': fields.Date.today()
        })
        return True