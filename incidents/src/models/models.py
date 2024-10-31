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
    
def cargar_datos_iniciales():
    insert_tipo_data()
    insert_estado_data()
    insert_canal_data()
    insert_incident_test()

def insert_tipo_data():
    tipos_data = [
        {'id': 1, 'tipo': 'Petición'},
        {'id': 2, 'tipo': 'Queja/Reclamo'},
        {'id': 3, 'tipo': 'Sugerencia'}
    ]

    for tipo_data in tipos_data:
        tipo_exists = Tipo.query.filter_by(id=tipo_data['id']).first()
        if not tipo_exists:
            new_tipo = Tipo(id=tipo_data['id'], tipo=tipo_data['tipo'])
            db.session.add(new_tipo)
            print(f"Insertando tipo: {tipo_data['tipo']}")
        else:
            print(f"Tipo '{tipo_data['tipo']}' ya existe en la base de datos.")

    db.session.commit()


def insert_estado_data():
    estados_data = [
        {'id': 1, 'estado': 'Abierto'},
        {'id': 2, 'estado': 'Desestimado'},
        {'id': 3, 'estado': 'Escalado'},
        {'id': 4, 'estado': 'Cerrado Satisfactoriamente'},
        {'id': 5, 'estado': 'Cerrado Insatisfactoriamente'},
        {'id': 6, 'estado': 'Reaperturado'}
    ]

    for estado_data in estados_data:
        estado_exists = Estado.query.filter_by(id=estado_data['id']).first()
        if not estado_exists:
            new_estado = Estado(id=estado_data['id'], estado=estado_data['estado'])
            db.session.add(new_estado)
            print(f"Insertando estado: {estado_data['estado']}")
        else:
            print(f"Estado '{estado_data['estado']}' ya existe en la base de datos.")

    db.session.commit()

def insert_canal_data():
    canales_data = [
        {'id': 1, 'nombre_canal': 'Llamada Telefónica', 'precio': 10000.0},
        {'id': 2, 'nombre_canal': 'Correo Electrónico', 'precio': 30000.0},
        {'id': 3, 'nombre_canal': 'App Movil', 'precio': 50000.0}
    ]

    for canal_data in canales_data:
        canal_exists = Canal.query.filter_by(id=canal_data['id']).first()
        if not canal_exists:
            new_canal = Canal(
                id=canal_data['id'],
                nombre_canal=canal_data['nombre_canal'],
                precio=canal_data['precio']
            )
            db.session.add(new_canal)
            print(f"Insertando canal: {canal_data['nombre_canal']}")
        else:
            print(f"Canal '{canal_data['nombre_canal']}' ya existe en la base de datos.")

    db.session.commit()
    
def insert_incident_test():
    incident_test = Incidente.query.filter(Incidente.codigo == 'INC00000').first()
    if not incident_test:
        incident = Incidente(
                  codigo = 'INC00000',
                  descripcion = 'Detalle incidencia INC00000',
                  asunto = 'Asunto incidencia INC0000',
                  canal_id = 1,
                  tipo_id = 1,
                  estado_id =  1,
                  usuario_creador_id = 1,
                  usuario_asignado_id = 1,
                  persona_id = 1
              )
        
        db.session.add(incident)
        db.session.commit()

        incident_history = HistoricoIncidencia(
                    observaciones = 'Se ha creado la incidencia INC00000 con exito',
                    incidencia_id = incident.id,
                    usuario_creador_id = 1,
                    estado_id = 1,
                    usuario_asignado_id = 1
        )
        
        db.session.add(incident_history)
        db.session.commit()

