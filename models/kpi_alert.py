from odoo import models, fields, api
from datetime import datetime, timedelta


class KpiAlert(models.Model):
    _name = 'kpi.alert'
    _description = 'KPI Alert System'

    name = fields.Char(string='Nombre de Alerta', required=True)
    alert_type = fields.Selection([
        ('project_delay', 'Retraso en Proyecto'),
        ('task_delay', 'Retraso en Tarea'),
        ('budget_exceeded', 'Presupuesto Excedido'),
        ('risk_high', 'Riesgo Alto'),
        ('completion_low', 'Bajo Porcentaje de Completado')
    ], string='Tipo de Alerta', required=True)

    project_id = fields.Many2one('kpi.project', string='Proyecto')
    task_id = fields.Many2one('kpi.task', string='Tarea')
    severity = fields.Selection([
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica')
    ], string='Severidad', required=True)

    message = fields.Text(string='Mensaje de Alerta')
    is_resolved = fields.Boolean(string='Resuelta', default=False)
    resolution_notes = fields.Text(string='Notas de Resolución')

    date_triggered = fields.Datetime(string='Fecha de Activación', default=fields.Datetime.now)
    date_resolved = fields.Datetime(string='Fecha de Resolución')

    def action_resolve_alert(self):
        self.write({
            'is_resolved': True,
            'date_resolved': fields.Datetime.now()
        })
        return True