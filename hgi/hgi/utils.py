
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






