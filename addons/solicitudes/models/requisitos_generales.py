# -*- coding: utf-8 -*-

from openerp import models, fields, api


class RequisitosGenerales(models.Model):
    _name = 'solicitudes.requisitos_generales'

    solicitudes_id = fields.Many2one('solicitudes.solicitudes', string="Número de expediente")
    documentos_generales_id = fields.Many2one('politicas.documentos_generales', string="Tipo de Documento")
    documento = fields.Binary(string='Documento')
    observaciones = fields.Char(string='Observaciones')
    valido = fields.Boolean(string='Valido')


