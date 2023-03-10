
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
            data['total_partida'] = partida.total
            data['total_used'] = partida.ingresado
            data['balance'] = partida.total - partida.ingresado
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