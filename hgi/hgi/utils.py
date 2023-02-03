
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
        
            








