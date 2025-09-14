from odoo import models, fields, api


class KpiExportWizard(models.TransientModel):
    _name = 'kpi.export.wizard'
    _description = 'KPI Export Wizard'

    export_format = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV')
    ], string='Formato de Exportación', default='pdf')

    include_tasks = fields.Boolean(string='Incluir Tareas', default=True)
    include_metrics = fields.Boolean(string='Incluir Métricas', default=True)

    def action_export(self):
        self.ensure_one()
        # Lógica de exportación aquí
        return {
            'type': 'ir.actions.act_url',
            'url': '/kpi/export',
            'target': 'self',
        }