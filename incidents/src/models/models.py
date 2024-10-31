from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()

class Incidente(db.Model):
    __tablename__ = 'incidente'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    asunto = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    canal_id = db.Column(db.Integer, db.ForeignKey('canal.id'), nullable=False)
    usuario_creador_id = db.Column(db.Integer, nullable=False)
    usuario_asignado_id = db.Column(db.Integer, nullable=False)
    persona_id = db.Column(db.Integer, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    
    estado = db.relationship('Estado', backref='incidentes')
    tipo = db.relationship('Tipo', backref='incidentes')
    
class Canal(db.Model):
    __tablename__ = 'canal'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_canal = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Double)
    

class Estado(db.Model):
    __tablename__ = 'estado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(50), nullable=False)

class Tipo(db.Model):
    __tablename__ = 'tipo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)
    

class Llamada(db.Model):
    __tablename__ = 'llamada'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_grabacion = db.Column(db.String(255), nullable=False)
    duracion = db.Column(db.String, nullable=False)
    fecha_hora_llamada = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    incidencia_id = db.Column(db.Integer, db.ForeignKey('incidente.id'), nullable=False)
    persona_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    
class HistoricoIncidencia(db.Model):
    __tablename__ = 'historico_incidencia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    observaciones = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    incidencia_id = db.Column(db.Integer, db.ForeignKey('incidente.id'), nullable=False)
    usuario_creador_id = db.Column(db.Integer, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    usuario_asignado_id = db.Column(db.Integer, nullable=False)
      
class Evidencia(db.Model):
    __tablename__ = 'evidencia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_adjunto = db.Column(db.String(100), nullable=False)
    formato = db.Column(db.String(100), nullable=False)
    tamano = db.Column(db.String(255), nullable=False)
    incidencia_id = db.Column(db.Integer, db.ForeignKey('incidente.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class EvidenciaHistorico(db.Model):
    __tablename__ = 'evidencia_historico'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evidencia_id = db.Column(db.Integer, db.ForeignKey('evidencia.id'), nullable=False)
    historico_id = db.Column(db.Integer, db.ForeignKey('historico_incidencia.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  
    evidencia = db.relationship('Evidencia', backref='evidencia_historicos')

class IncidenteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incidente
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class CanalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Canal
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class EstadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estado
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class TipoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tipo
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class LlamadaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Llamada
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class HistoricoIncidenciaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HistoricoIncidencia
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class EvidenciaHistoricoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EvidenciaHistorico
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
class EvidenciaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Evidencia
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
    
