
from hgi_static.models import GestionCambios
from hgi_users.models import User
from hgi_static.models import PermisoContratoUser
from hgi_ventas.serializer import PartidaSerializer
from hgi_ventas.models import Partida
from hgi_ventas.models import ProductoOC
from hgi_static.models import Contrato
from hgi_users.models import CargoUser
from hgi_users.models import UserToken


def get_user_from_usertoken(token):
    token = token.replace("Token ", "")
    user = UserToken.objects.get(token=token).user
    return user

def user_can_see_oc(user, oc):
    cargo = CargoUser.objects.get(id=user.position.id)
    if cargo.ver_oc:
        return True
    elif cargo.por_contrato:
        contrato = oc.contrato
        if user.id == contrato.responsable.id or user.id == contrato.administrador.id or user.id == contrato.visitador.id or user.id == contrato.of_tecnica.id or user.id == contrato.compras.id or user.id == contrato.administrativo.id or user.id == contrato.prevencionista.id:
            return True
    return False

def user_can_edit_oc(user, oc):
    cargo = CargoUser.objects.get(id=user.position.id)
    if cargo.modificar_oc:
        return True
    elif cargo.por_contrato:
        contrato = oc.contrato
        if user.id == contrato.responsable.id or user.id == contrato.administrador.id or user.id == contrato.visitador.id or user.id == contrato.of_tecnica.id or user.id == contrato.compras.id or user.id == contrato.administrativo.id or user.id == contrato.prevencionista.id:
            return True
    return False

def can_accept_oc(oc):
    part_dict = {}
    products = ProductoOC.objects.filter(oc=oc)
    can = True
    for product in products:
        data = {}
        partida = product.partida
        if partida.id in part_dict.keys():
            data = part_dict[product.partida.id]
            data['total_oc'] += product.total_precio()
            data['new_balance'] = data['balance'] - data['total_oc']
            part_dict[partida.id] = data
        else:
            productos = ProductoOC.objects.filter(partida=partida.id)
            partida_ingresado = 0
            for producto in productos:
                partida_ingresado += producto.total_precio()
            data['total_partida'] = partida.total
            data['total_used'] = partida_ingresado
            data['balance'] = partida.total - partida_ingresado
            data['total_oc'] = product.total_precio()
            data['new_balance'] = data['balance'] - data['total_oc']
            part_dict[partida.id] = data
    for partida_data in part_dict:
        if partida_data['new_balance'] < 0:
            can = False
    return can, part_dict

 
def get_total_partidas_APU(partidas):
    partidas = PartidaSerializer(partidas, many=True).data
    total_partidas = 0
    total_ingresado = 0
    for partida in partidas:
        total_partidas += partida['total']
        productos = ProductoOC.objects.filter(partida=partida['id'])
        for producto in productos:
            total_ingresado += producto.total_precio()
    return total_partidas, total_ingresado

def add_info_oc(oc, oc_data):

    oc_data['nombre_proveedor'] = oc.proveedor.rs
    oc_data['nombre_emisor'] = oc.emisor.short_name()
    oc_data['nombre_contrato'] = oc.contrato.nombre
    oc_data['nombre_estado'] = oc.estado.nombre
    oc_data['nombre_forma_pago'] = oc.forma_pago.descripcion
    oc_data['nombre_tipo'] = oc.tipo.descripcion
    oc_data['nombre_moneda'] = oc.moneda.simbolo 
    return

def create_contrato_user_permission(contrato_data):
    permissions = {}
    contrato = Contrato.objects.get(id=contrato_data['id'])

    if contrato.responsable.id not in permissions.keys():
        permissions[contrato.responsable.id] = [1,]
    else:
        permissions[contrato.responsable.id].append(1)

    if contrato.administrador.id not in permissions.keys():
        permissions[contrato.administrador.id] = [3,]
    else:
        permissions[contrato.administrador.id].append(3)

    if contrato.visitador.id not in permissions.keys():
        permissions[contrato.visitador.id] = [2,]
    else:
        permissions[contrato.visitador.id].append(2)
    
    if contrato.of_tecnica.id not in permissions.keys():
        permissions[contrato.of_tecnica.id] = [6,]
    else:
        permissions[contrato.of_tecnica.id].append(6)
    
    if contrato.compras.id not in permissions.keys():
        permissions[contrato.compras.id] = [5,]
    else:
        permissions[contrato.compras.id].append(5)

    if contrato.administrativo.id not in permissions.keys():
        permissions[contrato.administrativo.id] = [7,]
    else:
        permissions[contrato.administrativo.id].append(7)

    if contrato.prevencionista.id not in permissions.keys():
        permissions[contrato.prevencionista.id] = [4,]
    else:
        permissions[contrato.prevencionista.id].append(4)
     
    for key, permission in permissions.items():
        user = User.objects.get(id=key)
        PermisoContratoUser.objects.create(user=user,contrato=contrato,permisos=permission)

    return

def get_changes_list(data):
    changes = []

    if "nombre" in data.keys():
        changes.append(2)
    if "business_name" in data.keys():
        changes.append(2)
    if "codigo" in data.keys():
        changes.append(3)
    if "code" in data.keys():
        changes.append(3)
    if "direccion" in data.keys():
        changes.append(4)
    if "address" in data.keys():
        changes.append(4)
    if "estado" in data.keys():
        changes.append(5)
    if "tipo" in data.keys():
        changes.append(6)
    if "clasificacion" in data.keys():
        changes.append(7)
    if "obra" in data.keys():
        changes.append(8)
    if "glosa" in data.keys():
        changes.append(9)
    if "observacion" in data.keys():
        changes.append(10)
    if "auto_a" in data.keys():
        changes.append(11)
    if "auto_r" in data.keys():
        changes.append(12)
    if "activity" in data.keys():
        changes.append(13)
    if "rut" in data.keys():
        changes.append(14)
    if "phone" in data.keys():
        changes.append(15)
    if "telefono" in data.keys():
        changes.append(15)
    if "email" in data.keys():
        changes.append(16)
    if "mail_contacto" in data.keys():
        changes.append(16)
    if "contact" in data.keys():
        changes.append(17)
    if "contacto" in data.keys():
        changes.append(17)
    if "rs" in data.keys():
        changes.append(18)
    if "credito" in data.keys():
        changes.append(19)
    if "cuenta" in data.keys():
        changes.append(20)
    if "banco" in data.keys():
        changes.append(21)
    return changes 

def register_change(id,change_types,user,changed_model):
    types = {
        1: "Objeto Creado",
        2: "Objeto Editado (Nombre)",
        3: "Objeto Editado (Código)",
        4: "Objeto Editado (Dirección)",
        5: "Objeto Editado (Estado)",
        6: "Objeto Editado (Tipo)",
        7: "Objeto Editado (Clasificación)",
        8: "Objeto Editado (Obra)",
        9: "Objeto Editado (Glosa)",
        10: "Objeto Editado (Observación)",
        11: "Orden de Compra Autorizada (A)",
        12: "Orden de Compra Autorizada (R)",
        13: "Objeto Editado (Actividad)",
        14: "Objeto Editado (Rut)",
        15: "Objeto Editado (Teléfono)",
        16: "Objeto Editado (Email)",
        17: "Objeto Editado (Contacto)",
        18: "Objeto Editado (Razón Social)",
        19: "Objeto Editado (Crédito)",
        20: "Objeto Editado (Cuenta)",
        21: "Objeto Editado (Banco)",
    }
    for change_type in change_types:
        GestionCambios.objects.create(type_model=changed_model, obj_id=id, accion=types[change_type], user=user)
    
    return