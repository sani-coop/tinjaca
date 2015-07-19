-*- coding: utf-8 -*-

from openerp import models, fields, api

class Solicitantes(models.Model):
    _name = 'propuestas.solicitantes'

    propuesta_id = fields.One2many('propuestas.propuestas', string="Propuesta")
    codigo_solicitud = fields.Char(string='Codigo de la Solicitud', required=True)
    nombres = fields.Char(string='Nombres del Solicitante', required=True)
    apellidos = fields.Char(string='Apellidos del Solicitante', required=True)
    ci = fields.Integer(string='CI del Solicitante', required=True)
    rif = fields.Char(string='RIF del Solicitante', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required=True)
    edad = fields.Integer(string='Edad del Solicitante', required=True)
    sexo = fields.Char(string='Sexo del Solicitante', required=True)
    direccion_habitacion = fields.Char(string='Direccion de Habitacion', required=True)
    municipio = fields.Char(string='Municipio', required=True)
    parroquia = fields.Char(string='Parroquia', required=True)
    profesion_oficio = fields.Char(string='Profesion u Oficio', required=True)
    telefono_fijo = fields.Integer(string='Telefono Fijo', required=True)
    telefono_celular = fields.Integer(string='Telefono Celular', required=True)
    correo_electronico = fields.Char(string='Correo Electronico', required=True)
