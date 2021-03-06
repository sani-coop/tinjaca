# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Solicitudes(models.Model):
    _name = 'solicitudes.solicitudes'

    _rec_name = 'nro_expediente'

    propuestas_id = fields.Many2one('propuestas.propuestas', string="Propuesta", required=True)

    sector_id = fields.Many2one('politicas.sectores', string="Sector", required=True)
    nro_expediente = fields.Char(string='Numero de expediente', required=True) #TODO calculado!!!

    # Campos provinientes de propuestas:
    propuestas_solicitantes_id = fields.Many2one(string='Solicitante', related='propuestas_id.solicitantes_id', readonly=True)
    propuestas_tipos_garantia_id = fields.Many2one(related='propuestas_id.tipos_garantia_id', string="Tipo de Garantia")
    propuestas_empresa_establecida = fields.Boolean(related='propuestas_id.up_empresa_establecida', readonly=True)

    # Campos para los montos y tasas:
    monto_total = fields.Float(string='Monto total')
    plazo_pago = fields.Integer(string='Periodo de pago')
    forma_pago_id = fields.Many2one('politicas.forma_pago',string='Forma de pago')
    periodos_gracia = fields.Integer(string='Periodo de gracia')
    tasa_interes = fields.Float(string='Tasa de interes')
    tasa_mora = fields.Float(string='Tasa de mora')
    #monto_cuota = fields.Float(string='Monto de la cuota') #calculado
    comision_flat = fields.Float(string='Comision FLAT')
    aporte_social = fields.Float(string='Aporte social')

    # Campos para generar del documento de credito y de la empresa
    fecha_de_entrega = fields.Date("Fecha de Entrega")
    lapso_de_devolucion = fields.Integer(string='Lapso de devolucion del documento')

    # Campos de liquidacion de credito
    fecha_liquidacion = fields.Date(string='Fecha de liquidacion')
    fecha_ultima = fields.Date(string='Fecha ultima de pago') #calculado

    # Referencias a otros modelos:
    requisitos_generales_id = fields.One2many('solicitudes.requisitos_generales', 'solicitudes_id', string="Requisitos generales")
    requisitos_sector_id = fields.One2many('solicitudes.requisitos_sector', 'solicitudes_id', string="Requisitos sector")
    requisitos_garantia_id = fields.One2many('solicitudes.requisitos_garantia', 'solicitudes_id', string="Requisitos garantia")
    requisitos_empresa_id = fields.One2many('solicitudes.requisitos_empresa', 'solicitudes_id', string="Requisitos empresa")
    control_previo_id = fields.One2many('solicitudes.control_previo', 'solicitudes_id', string="Control Previo")
    avaluo_id = fields.One2many('solicitudes.avaluo', 'solicitudes_id', string="Avaluo")
    inspeccion_id = fields.One2many('solicitudes.inspecciones', 'solicitudes_id', string="Inspeccion")
    informe_tecnico_id = fields.One2many('solicitudes.informe_tecnico', 'solicitudes_id', string="Informe tecnico")
    observaciones_ids = fields.One2many('solicitudes.observaciones_estaciones', 'solicitudes_id', string="Observaciones de la estacion")
    consejos_directivos_ids = fields.Many2many('consejos.consejos', string="Consejo directivo", relation='consejos_consejos_solicitudes_rel')
    #cuentas_cobrar_ids = fields.One2many('administracion.cuentas_cobrar', string="Cuenta por cobrar") #Error!!!
    #cheques_ids = fields.One2many('administracion.cheques', 'solicitudes_id', string="Cuenta por cobrar") #Error!!!

    state = fields.Selection(string='Estacion',
                             selection=[('estacion_1_consignacion_requisitos', 'Consignacion de Requisitos'),
                                        ('estacion_2_control_previo', 'Control Previo'),
                                        ('estacion_3_inspeccion_avaluo', 'Inspeccion / Avaluo'),
                                        ('estacion_4_evaluacion_gerente', 'Evaluacion por Gerente'),
                                        ('estacion_5_evaluacion_presidencia', 'Evaluacion por Presidencia'),
                                        ('estacion_6_discusion_consejo', 'Discusion por Consejo'),
                                        ('estacion_7_creacion_documentos', 'Creacion Documentos'),
                                        ('estacion_8_liquidacion', 'Liquidacion'),
                                        ('estacion_9_acompanamiento', 'Acompanamiento'),
                                        ('estacion_10_recuperaciones', 'Recuperaciones'),
                                        ('estacion_11_consultoria_juridica', 'Consultoria Juridica'),
                                        ('estacion_12_archivo', 'Archivo')],
                             default='estacion_1_consignacion_requisitos')

    estatus_requisitos = fields.Selection(string='Estatus Requisitos',
                                          selection=[('estatus_asignar', 'Por asignar'),
                                                     ('estatus_pendiente', 'Pendiente'),
                                                     ('estatus_completo', 'Completo'),
                                                     ('estatus_deficiente', 'Deficiente'),
                                                     ('estatus_devuelto', 'Devuelto')],
                                          default='estatus_asignar')

    estatus_juridico = fields.Selection(string='Estatus Juridico',
                                        selection=[('estatus_asignar', 'Por asignar'),
                                                   ('estatus_aceptado_juridico', 'Aceptado'),
                                                   ('estatus_rechazado_juridico', 'Rechazado'),
                                                   ('estatus_aceptado_cond_juridico', 'Aceptado condicionado'),
                                                   ('estatus_devuelto', 'Devuelto')],
                                        default='estatus_asignar')

    estatus_economico = fields.Selection(string='Estatus Economico',
                                         selection=[('estatus_asignar', 'Por asignar'),
                                                    ('estatus_negado_economico', 'Negado'),
                                                    ('estatus_aprobado_economico', 'Aprobado'),
                                                    ('estatus_aprobado_cond_economico', 'Aprobado Condicionado'),
                                                    ('estatus_devuelto', 'Devuelto')],
                                         default='estatus_asignar')

    estatus_gerencia_credito = fields.Selection(string='Estatus Gerencia',
                                                selection=[('estatus_evaluar', 'Por evaluar'),
                                                           ('estatus_negado_gerencia', 'Negado'),
                                                           ('estatus_aprobado_gerencia', 'Aprobado'),
                                                           ('estatus_aprobado_cond_gerencia', 'Aprobado Condicionado'),
                                                           ('estatus_devuelto_a_requisitos', 'Devuelto a requisitos'),
                                                           ('estatus_devuelto_a_control_previo', 'Devuelto a control previo'),
                                                           ('estatus_devuelto_a_avaluo', 'Devuelto a avaluo')],
                                                default='estatus_evaluar')

    estatus_presidencia = fields.Selection(string='Estatus Presidencia',
                                           selection=[('estatus_decidir', 'Por decidir'),
                                                      ('estatus_recomendado', 'Recomendado'),
                                                      ('estatus_no_recomendado', 'No recomendado'),
                                                      ('estatus_recomendado_cond', 'Recomendado Condicionado'),
                                                      ('estatus_devuelto', 'Devuelto')],
                                           default='estatus_decidir')

    estatus_consejo_directivo = fields.Selection(string='Estatus Consejo',
                                                 selection=[('estatus_discutir', 'Por discutir'),
                                                            ('estatus_negado_consejo', 'Negado'),
                                                            ('estatus_aprobado_consejo', 'Aprobado'),
                                                            ('estatus_aprobado_cond_consejo', 'Aprobado Condicionado'),
                                                            ('estatus_diferido', 'Diferido'),
                                                            ('estatus_devuelto', 'Devuelto')],
                                                 default='estatus_discutir')

    estatus_secretaria = fields.Selection(string='Estatus Secretaria',
                                          selection=[('estatus_asignar', 'Por asignar'),
                                                     ('estatus_entrego', 'Entrego'),
                                                     ('estatus_no_entrego', 'No entrego')],
                                          default='estatus_asignar')

    estatus_liquidacion = fields.Selection(string='Estatus Liquidacion',
                                           selection=[('estatus_asignar', 'Por asignar'),
                                                      ('estatus_liquidado', 'Liquidado'),
                                                      ('estatus_devuelto', 'Devuelto')],
                                           default='estatus_asignar')

    estatus_acompanamiento = fields.Selection(string='Estatus Acompanamiento',
                                              selection=[('estatus_asignar', 'Por asignar'),
                                                         ('estatus_invirtio', 'Invirtio'),
                                                         ('estatus_no_invirtio', 'No invirtio'),
                                                         ('estatus_devuelto', 'Devuelto')],
                                              default='estatus_asignar')

    estatus_recuperaciones = fields.Selection(string='Estatus recuperaciones',
                                              selection=[('estatus_asignar', 'Por asignar'),
                                                         ('estatus_caja', 'Caja'),
                                                         ('estatus_liberar', 'Liberar'),
                                                         ('estatus_demandar', 'Demandar'),
                                                         ('estatus_extrajudicial', 'Extrajudicial'),
                                                         ('estatus_devuelto', 'Devuelto')],
                                              default='estatus_asignar')

    estatus_consultoria_juridica = fields.Selection(string='Estatus consultoria juridica',
                                                    selection=[('estatus_asignar', 'Por asignar'),
                                                               ('estatus_liberado', 'Liberado'),
                                                               ('estatus_demandado', 'Demandado'),
                                                               ('estatus_reintegrado', 'Reintegrado'),
                                                               ('estatus_devuelto', 'Devuelto')],
                                                    default='estatus_asignar')

    estatus_archivo = fields.Selection(string='Estatus archivo',
									   selection=[('estatus_asignar', 'Por asignar'),
                                                  ('estatus_devuelto_a_gerencia', 'Devuelto a gerencia'),
                                                  ('estatus_devuelto_a_creacion_doc', 'Devuelto a creacion de documentos'),
                                                  ('estatus_devuelto_a_administracion', 'Devuelto a administracion')],
                                       default='estatus_asignar')

    # Cambia a la estacion "Consignar Requisitos"
    @api.one
    def action_estacion_consignacion_requisitos(self):
        self.state = 'estacion_1_consignacion_requisitos'

    # Cambia a la estacion "Control Previo"
    @api.one
    def action_estacion_control_previo(self):
        self.state = 'estacion_2_control_previo'

    # Cambia a la estacion "Inspeccion - Avaluo"
    @api.one
    def action_estacion_inspeccion_avaluo(self):
        self.state = 'estacion_3_inspeccion_avaluo'

    # Cambia a la estacion "Aprobacion Gerente"
    @api.one
    def action_estacion_evaluacion_gerente(self):
        self.state = 'estacion_4_evaluacion_gerente'

    # Cambia a la estacion "Aprobacion Secretaria"
    @api.one
    def action_estacion_evaluacion_presidencia(self):
        self.state = 'estacion_5_evaluacion_presidencia'

    # Cambia a la estacion "Aprobacion Consejo"
    @api.one
    def action_estacion_discusion_consejo(self):
        self.state = 'estacion_6_discusion_consejo'

    # Cambia a la estacion "Creacion Documentos"
    @api.one
    def action_estacion_creacion_documentos(self):
        self.state = 'estacion_7_creacion_documentos'

    # Cambia a la estacion "Liquidacion"
    @api.one
    def action_estacion_liquidacion(self):
        self.state = 'estacion_8_liquidacion'

    # Cambia a la estacion "Acompanamiento"
    @api.one
    def action_estacion_acompanamiento(self):
        self.state = 'estacion_9_acompanamiento'

    # Cambia a la estacion "recuperaciones"
    @api.one
    def action_estacion_recuperaciones(self):
        self.state = 'estacion_10_recuperaciones'

    # Cambia a la estacion "consultoria juridica"
    @api.one
    def action_estacion_consultoria(self):
        self.state = 'estacion_11_consultoria_juridica'

    # Cambia a la estacion "archivo"
    @api.one
    def action_estacion_archivo(self):
        self.state = 'estacion_12_archivo'



    # Cambia al estatus "Asignar" (requisitos)
    @api.one
    def action_estatus_asignar_requisitos(self):
        self.estatus_requisitos = 'estatus_asignar'

    # Cambia al estatus "Pendiente" (requisitos)
    @api.one
    def action_estatus_pendiente_requisitos(self):
        self.estatus_requisitos = 'estatus_pendiente'

    # Cambia al estatus "Completo" (requisitos)
    @api.one
    def action_estatus_completo_requisitos(self):
        self.estatus_requisitos = 'estatus_completo'

    # Cambia al estatus "Deficiente" (requisitos)
    @api.one
    def action_estatus_deficiente_requisitos(self):
        self.estatus_requisitos = 'estatus_deficiente'

    # Cambia al estatus "Devuelto" (requisitos)
    @api.one
    def action_estatus_devuelto_requisitos(self):
        self.estatus_requisitos = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (juridico)
    @api.one
    def action_estatus_asignar_juridico(self):
        self.estatus_juridico = 'estatus_asignar'

    # Cambia al estatus "Aceptar" (juridico)
    @api.one
    def action_estatus_aceptar_juridico(self):
        self.estatus_juridico = 'estatus_aceptado_juridico'

    # Cambia al estatus "Rechazar" (juridico)
    @api.one
    def action_estatus_rechazar_juridico(self):
        self.estatus_juridico = 'estatus_rechazado_juridico'

    # Cambia al estatus "Aceptar con condicion" (juridico)
    @api.one
    def action_estatus_aceptar_cond_juridico(self):
        self.estatus_juridico = 'estatus_aceptado_cond_juridico'

    # Cambia al estatus "Devuelto" (juridico)
    @api.one
    def action_estatus_devuelto_juridico(self):
        self.estatus_juridico = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (economico)
    @api.one
    def action_estatus_asignar_economico(self):
        self.estatus_economico = 'estatus_asignar'

    # Cambia al estatus "Negado" (economico)
    @api.one
    def action_estatus_negado_economico(self):
        self.estatus_economico = 'estatus_negado_economico'

    # Cambia al estatus "Aprobado" (economico)
    @api.one
    def action_estatus_aprobado_economico(self):
        self.estatus_economico = 'estatus_aprobado_economico'

    # Cambia al estatus "Aprobado condicionado" (economico)
    @api.one
    def action_estatus_aprobado_cond_economico(self):
        self.estatus_economico = 'estatus_aprobado_cond_economico'

    # Cambia al estatus "Devuelto" (economico)
    @api.one
    def action_estatus_devuelto_economico(self):
        self.estatus_economico = 'estatus_devuelto'


    # Cambia al estatus "Evaluar" (gerencia)
    @api.one
    def action_estatus_evaluar_gerencia(self):
        self.estatus_gerencia_credito = 'estatus_evaluar'

    # Cambia al estatus "Negado" (gerencia)
    @api.one
    def action_estatus_negado_gerencia(self):
        self.estatus_gerencia_credito = 'estatus_negado_gerencia'

    # Cambia al estatus "Aprobado" (gerencia)
    @api.one
    def action_estatus_aprobado_gerencia(self):
        self.estatus_gerencia_credito = 'estatus_aprobado_gerencia'

    # Cambia al estatus "Aprobado Condicionado" (gerencia)
    @api.one
    def action_estatus_aprobado_cond_gerencia(self):
        self.estatus_gerencia_credito = 'estatus_aprobado_cond_gerencia'

    # Cambia al estatus "devuelto_a_requisitos" (gerencia) 
    @api.one
    def action_devolver_gerencia_a_requisitos(self):
        self.estatus_gerencia_credito = 'estatus_devuelto_a_requisitos'

    # Cambia al estatus "devuelto_a_control_previo" (gerencia) 
    @api.one
    def action_devolver_gerencia_a_control_previo(self):
        self.estatus_gerencia_credito = 'estatus_devuelto_a_control_previo'

    # Cambia al estatus "devuelto_a_avaluo" (gerencia)
    @api.one
    def action_devolver_gerencia_a_avaluo(self):
        self.estatus_gerencia_credito = 'estatus_devuelto_a_avaluo'



    # Cambia al estatus "Decidir" (presidencia)
    @api.one
    def action_estatus_decidir_presidencia(self):
        self.estatus_presidencia = 'estatus_decidir'

    # Cambia al estatus "Recomendado" (presidencia)
    @api.one
    def action_estatus_recomendado_presidencia(self):
        self.estatus_presidencia = 'estatus_recomendado'

    # Cambia al estatus "No recomendado" (presidencia)
    @api.one
    def action_estatus_no_recomendado_presidencia(self):
        self.estatus_presidencia = 'estatus_no_recomendado'

    # Cambia al estatus "Recomendado Condicionado" (presidencia)
    @api.one
    def action_estatus_recomendado_cond_presidencia(self):
        self.estatus_presidencia = 'estatus_recomendado_cond'

    # Cambia al estatus "Devuelto" (presidencia)
    @api.one
    def action_estatus_devuelto_presidencia(self):
        self.estatus_presidencia = 'estatus_devuelto'


    # Cambia al estatus "Discutir" (consejo)
    @api.one
    def action_estatus_discutir_consejo(self):
        self.estatus_consejo_directivo = 'estatus_discutir'

    # Cambia al estatus "Negado" (consejo)
    @api.one
    def action_estatus_negado_consejo(self):
        self.estatus_consejo_directivo = 'estatus_negado_consejo'

    # Cambia al estatus "Aprobado" (consejo)
    @api.one
    def action_estatus_aprobado_consejo(self):
        self.estatus_consejo_directivo = 'estatus_aprobado_consejo'

    # Cambia al estatus "Aprobado Condicionado" (consejo)
    @api.one
    def action_estatus_aprobado_cond_consejo(self):
        self.estatus_consejo_directivo = 'estatus_aprobado_cond_consejo'

    # Cambia al estatus "Diferido" (consejo)
    @api.one
    def action_estatus_diferido_consejo(self):
        self.estatus_consejo_directivo = 'estatus_diferido'

    # Cambia al estatus "Devuelto" (consejo)
    @api.one
    def action_estatus_devuelto_consejo(self):
        self.estatus_consejo_directivo = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (secretaria)
    @api.one
    def action_estatus_asignar_secretaria(self):
        self.estatus_secretaria = 'estatus_asignar'

    # Cambia al estatus "Entrego" (secretaria)
    @api.one
    def action_estatus_entrego_secretaria(self):
        self.estatus_secretaria = 'estatus_entrego'

    # Cambia al estatus "No entrego" (secretaria)
    @api.one
    def action_estatus_no_entrego_secretaria(self):
        self.estatus_secretaria = 'estatus_no_entrego'



    # Cambia al estatus "Asignar" (Administracion)
    @api.one
    def action_estatus_asignar_administracion(self):
        self.estatus_liquidacion = 'estatus_asignar'

    # Cambia al estatus "Liquidado" (Administracion)
    @api.one
    def action_estatus_liquidado_administracion(self):
        self.estatus_liquidacion = 'estatus_liquidado'

    # Cambia al estatus "Devuelto" (Administracion)
    @api.one
    def action_estatus_devuelto_administracion(self):
        self.estatus_liquidacion = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (Acompanamiento)
    @api.one
    def action_estatus_asignar_acompanamiento(self):
        self.estatus_acompanamiento = 'estatus_asignar'

    # Cambia al estatus "Invirtio" (Acompanamiento)
    @api.one
    def action_estatus_invirtio_acompanamiento(self):
        self.estatus_acompanamiento = 'estatus_invirtio'

    # Cambia al estatus "No Invirtio" (Acompanamiento)
    @api.one
    def action_estatus_no_invirtio_acompanamiento(self):
        self.estatus_acompanamiento = 'estatus_no_invirtio'

    # Cambia al estatus "Devuelto" (Acompanamiento)
    @api.one
    def action_estatus_devuelto_acompanamiento(self):
        self.estatus_acompanamiento = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (Recuperaciones)
    @api.one
    def action_estatus_asignar_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_asignar'

    # Cambia al estatus "Caja" (Recuperaciones)
    @api.one
    def action_estatus_caja_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_caja'

    # Cambia al estatus "Liberar" (Recuperaciones)
    @api.one
    def action_estatus_liberar_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_liberar'

    # Cambia al estatus "Demandar" (Recuperaciones)
    @api.one
    def action_estatus_demandar_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_demandar'

    # Cambia al estatus "Extrajudicial" (Recuperaciones)
    @api.one
    def action_estatus_extrajudicial_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_extrajudicial'

    # Cambia al estatus "Devuelto" (Recuperaciones)
    @api.one
    def action_estatus_devuelto_recuperaciones(self):
        self.estatus_recuperaciones = 'estatus_devuelto'



    # Cambia al estatus "Asignar" (Consultoria Juridica)
    @api.one
    def action_estatus_asignar_consultoria(self):
        self.estatus_consultoria_juridica = 'estatus_asignar'

    # Cambia al estatus "Liberado" (Consultoria Juridica)
    @api.one
    def action_estatus_liberar_consultoria(self):
        self.estatus_consultoria_juridica = 'estatus_liberado'

    # Cambia al estatus "Demandado" (Consultoria Juridica)
    @api.one
    def action_estatus_demandar_consultoria(self):
        self.estatus_consultoria_juridica = 'estatus_demandado'

    # Cambia al estatus "Reintegro" (Consultoria Juridica)
    @api.one
    def action_estatus_reintegrar_consultoria(self):
        self.estatus_consultoria_juridica = 'estatus_reintegrado'

    # Cambia al estatus "Devolucion" (Consultoria Juridica)
    @api.one
    def action_estatus_devolver_consultoria(self):
        self.estatus_consultoria_juridica = 'estatus_devuelto'



    # Cambia al estatus "asignar" (Archivo)
    @api.one
    def action_estatus_devolver_arch_a_gerencia(self):
        self.estatus_archivo = 'estatus_devuelto_a_gerencia'

    # Cambia al estatus "asignar" (Archivo)
    @api.one
    def action_estatus_devol_arch_a_creacion_doc(self):
        self.estatus_archivo = 'estatus_devuelto_a_creacion_doc'

    # Cambia al estatus "asignar" (Archivo)
    @api.one
    def action_estatus_devol_arch_a_admin(self):
        self.estatus_archivo = 'estatus_devuelto_a_administracion'

    _sql_constraints = [
        ('numero_expediente_unico', 'unique(nro_expediente)', 'El numero de expediente ya existe!')
    ]


    # display_name = fields.Char(
    #     string='Número de expediente', compute='_compute_display_name',
    # )
    #
    # @api.one
    # @api.depends('nro_expediente')
    # def _compute_display_name(self):
    #     self.display_name = self.nro_expediente

