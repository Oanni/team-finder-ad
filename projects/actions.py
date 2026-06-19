from http import HTTPStatus

from django.http import JsonResponse

from projects.models import Project


def _missing_venture():
    return JsonResponse(
        {'status': 'error', 'message': 'Проект не найден'},
        status=HTTPStatus.NOT_FOUND,
    )


def _forbidden_action(message):
    return JsonResponse(
        {'status': 'error', 'message': message},
        status=HTTPStatus.FORBIDDEN,
    )


def _bad_request(message):
    return JsonResponse(
        {'status': 'error', 'message': message},
        status=HTTPStatus.BAD_REQUEST,
    )


def flip_bookmark(actor, venture_id):
    """Переключает признак избранного для проекта."""

    venture = Project.objects.filter(pk=venture_id).first()
    if venture is None:
        return _missing_venture()

    already_marked = actor.favorites.filter(id=venture.id).exists()

    if already_marked:
        actor.favorites.remove(venture)
    else:
        actor.favorites.add(venture)

    return JsonResponse({'status': 'ok', 'favorited': not already_marked})


def finalize_open_venture(actor, venture_id):
    """Закрывает открытый проект, если запрос от владельца."""

    venture = Project.objects.filter(pk=venture_id).first()
    if venture is None:
        return _missing_venture()

    if venture.owner != actor:
        return _forbidden_action('У вас нет прав на это действие')

    if venture.status != venture.STATUS_OPEN:
        return _bad_request('Проект уже завершён')

    venture.status = venture.STATUS_CLOSED
    venture.save(update_fields=['status'])

    return JsonResponse({
        'status': 'ok',
        'project_status': venture.STATUS_CLOSED,
    })


def flip_membership(actor, venture_id):
    """Добавляет или убирает участника из открытого проекта."""

    venture = Project.objects.filter(pk=venture_id).first()
    if venture is None:
        return _missing_venture()

    if venture.status != venture.STATUS_OPEN:
        return _bad_request('Нельзя участвовать в закрытом проекте')

    if venture.owner == actor:
        return _bad_request('Организатор не может покинуть собственный проект')

    already_joined = actor.participated_projects.filter(id=venture.id).exists()

    if already_joined:
        actor.participated_projects.remove(venture)
    else:
        actor.participated_projects.add(venture)

    return JsonResponse({'status': 'ok', 'participant': not already_joined})
