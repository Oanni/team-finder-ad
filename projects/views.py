from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.actions import finalize_open_venture, flip_bookmark, flip_membership
from projects.forms import VentureDraftForm
from projects.identifiers import VENTURE_PAGE_SIZE
from projects.models import Project
from projects.queries import bookmarked_by, catalog_queryset
from team_finder.paging import slice_for_page


def _paginated_ventures(http_request, queryset):
    return slice_for_page(http_request, queryset, VENTURE_PAGE_SIZE)


def browse_ventures(http_request):
    """Главная: каталог всех проектов."""

    page = _paginated_ventures(http_request, catalog_queryset())
    return render(http_request, 'projects/project_list.html', {'page_obj': page})


@login_required
def display_saved_ventures(http_request):
    """Личный список избранных проектов."""

    page = _paginated_ventures(http_request, bookmarked_by(http_request.user))
    return render(http_request, 'projects/favorite_projects.html', {'projects': page})


def _viewer_flags(http_request, venture):
    actor = http_request.user
    flags = {
        'is_participant': False,
        'is_owner': False,
        'is_favorited': False,
    }

    if not actor.is_authenticated:
        return flags

    flags['is_participant'] = venture.participants.filter(pk=actor.pk).exists()
    flags['is_owner'] = venture.owner == actor
    flags['is_favorited'] = actor.favorites.filter(pk=venture.pk).exists()
    return flags


def display_venture_detail(http_request, pk):
    """Карточка проекта с контекстом для шаблона."""

    venture = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=pk,
    )
    context = {'project': venture, **_viewer_flags(http_request, venture)}
    return render(http_request, 'projects/project-details.html', context)


def _render_draft(http_request, bound_form, editing):
    return render(
        http_request,
        'projects/create-project.html',
        {'form': bound_form, 'is_edit': editing},
    )


@login_required
def publish_venture(http_request):
    """Создание нового проекта от имени текущего участника."""

    actor = http_request.user

    if http_request.method != 'POST':
        return _render_draft(http_request, VentureDraftForm(), editing=False)

    submission = VentureDraftForm(http_request.POST)

    if not submission.is_valid():
        return _render_draft(http_request, submission, editing=False)

    venture = submission.save(commit=False)
    venture.owner = actor
    venture.save()
    venture.participants.add(actor)
    return redirect('projects:detail', pk=venture.pk)


def _assert_owner(venture, actor):
    if venture.owner != actor:
        raise PermissionDenied("Вы не можете редактировать этот проект")


@login_required
def amend_venture(http_request, pk):
    """Правка существующего проекта владельцем."""

    actor = http_request.user
    venture = get_object_or_404(Project, pk=pk)
    _assert_owner(venture, actor)

    if http_request.method != 'POST':
        return _render_draft(
            http_request,
            VentureDraftForm(instance=venture),
            editing=True,
        )

    submission = VentureDraftForm(http_request.POST, instance=venture)

    if submission.is_valid():
        saved = submission.save()
        return redirect('projects:detail', pk=saved.pk)

    return _render_draft(http_request, submission, editing=True)


@login_required
@require_POST
def flip_bookmark_state(http_request, pk):
    return flip_bookmark(http_request.user, pk)


@login_required
@require_POST
def finalize_venture(http_request, pk):
    return finalize_open_venture(http_request.user, pk)


@login_required
@require_POST
def flip_membership_state(http_request, pk):
    return flip_membership(http_request.user, pk)
