
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
            productos = ProductoOC.objects.filter(partida=partida['id'])
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
        print("NO -> responsable " + str(contrato.responsable.id))
        permissions[contrato.responsable.id] = [1,]
    else:
        print("SI -> responsable " + str(contrato.responsable.id))
        print(permissions[contrato.responsable.id])
        permissions[contrato.responsable.id] = permissions[contrato.responsable.id].append(1)

    if contrato.administrador.id not in permissions.keys():
        print("NO -> administrador " + str(contrato.administrador.id))
        permissions[contrato.administrador.id] = [3,]
    else:
        print("SI -> administrador " + str(contrato.administrador.id))
        print(permissions[contrato.administrador.id])
        permissions[contrato.administrador.id] = permissions[contrato.administrador.id].append(3)

    if contrato.visitador.id not in permissions.keys():
        print("NO -> visitador " + str(contrato.visitador.id))
        permissions[contrato.visitador.id] = [2,]
    else:
        print("SI -> visitador " + str(contrato.visitador.id))
        print(permissions[contrato.visitador.id])
        permissions[contrato.visitador.id] = permissions[contrato.visitador.id].append(2)
    
    if contrato.of_tecnica.id not in permissions.keys():
        print("NO -> of_tecnica " + str(contrato.of_tecnica.id))
        permissions[contrato.of_tecnica.id] = [6,]
    else:
        print("SI -> of_tecnica " + str(contrato.of_tecnica.id))
        print(permissions[contrato.of_tecnica.id])
        permissions[contrato.of_tecnica.id] = permissions[contrato.of_tecnica.id].append(6)
    
    if contrato.compras.id not in permissions.keys():
        print("NO -> compras " + str(contrato.compras.id))
        permissions[contrato.compras.id] = [5,]
    else:
        print("SI -> compras " + str(contrato.compras.id))
        print(permissions[contrato.compras.id])
        permissions[contrato.compras.id] = permissions[contrato.compras.id].append(5)

    if contrato.administrativo.id not in permissions.keys():
        print("NO -> administrativo " + str(contrato.administrativo.id))
        permissions[contrato.administrativo.id] = [7,]
    else:
        print("SI -> administrativo " + str(contrato.administrativo.id))
        print(permissions[contrato.administrativo.id])
        permissions[contrato.administrativo.id] = permissions[contrato.administrativo.id].append(7)

    if contrato.prevencionista.id not in permissions.keys():
        print("NO -> prevencionista " + str(contrato.prevencionista.id))
        permissions[contrato.prevencionista.id] = [4,]
    else:
        print("SI -> prevencionista " + str(contrato.prevencionista.id))
        print(permissions[contrato.prevencionista.id])
        permissions[contrato.prevencionista.id] = permissions[contrato.prevencionista.id].append(4)
    
    for key, permission in permissions.items():
        PermisoContratoUser.objects.create(user=key,contrato=contrato.id,permisos=permission)

    return