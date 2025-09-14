from odoo import models, fields, api


class KpiTask(models.Model):
    _name = 'kpi.task'
    _description = 'KPI Task - Professional Edition'
    _order = 'priority desc, sequence asc'

    name = fields.Char(string='Nombre de la Tarea', required=True)
    project_id = fields.Many2one('kpi.project', string='Proyecto', required=True)
    sequence = fields.Integer(string='Secuencia', default=10)

    assigned_to = fields.Char(string='Asignada A', required=True)
    start_date = fields.Date(string='Fecha de Inicio', default=fields.Date.today)
    end_date = fields.Date(string='Fecha de Finalización')

    duration = fields.Integer(string='Duración (días)', compute='_compute_duration', store=True)
    cost = fields.Float(string='Costo', digits=(16, 2))

    state = fields.Selection([
        ('not_started', 'No iniciada'),
        ('in_progress', 'En curso'),
        ('completed', 'Completada'),
        ('delayed', 'Atrasada'),
        ('on_hold', 'En espera')
    ], string='Estado', default='not_started')

    risk = fields.Selection([
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja')
    ], string='Riesgo', default='medium')

    priority = fields.Selection([
        ('high', 'Alta'),
        ('medium', 'Media'),
        ('low', 'Baja')
    ], string='Prioridad', default='medium')

    comments = fields.Text(string='Comentarios')
    progress = fields.Integer(string='Progreso (%)', default=0)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for task in self:
            if task.start_date and task.end_date:
                start = fields.Date.from_string(task.start_date)
                end = fields.Date.from_string(task.end_date)
                task.duration = (end - start).days + 1
            else:
                task.duration = 0

    def action_start_task(self):
        self.write({'state': 'in_progress'})
        return True

    def action_complete_task(self):
        self.write({'state': 'completed', 'progress': 100})
        return True