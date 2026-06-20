from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from projects.models import Project
from team_finder.paging import slice_for_page
from users.identifiers import (
    ADMIRERS_OF_MINE_KEY,
    CATALOG_FILTER_LABELS,
    FAVORITE_OWNERS_KEY,
    JOINED_VENTURE_OWNERS_KEY,
    MEMBER_PAGE_SIZE,
    MY_VENTURE_MEMBERS_KEY,
)

Member = get_user_model()


def _base_roster():
    return (
        Member.objects
        .prefetch_related(
            Prefetch(
                'owned_projects',
                queryset=Project.objects.select_related('owner'),
            ),
            'favorites',
            'participated_projects',
        )
        .order_by('-date_joined')
    )


def _apply_catalog_filter(roster, viewer, filter_key):
    if filter_key == FAVORITE_OWNERS_KEY:
        return roster.filter(owned_projects__interested_users=viewer)
    if filter_key == JOINED_VENTURE_OWNERS_KEY:
        return roster.filter(owned_projects__participants=viewer)
    if filter_key == ADMIRERS_OF_MINE_KEY:
        return roster.filter(favorites__owner=viewer)
    if filter_key == MY_VENTURE_MEMBERS_KEY:
        return roster.filter(participated_projects__owner=viewer)
    return roster


def _should_filter(viewer, filter_key):
    return viewer.is_authenticated and bool(filter_key)


def assemble_member_catalog(http_request):
    """Формирует страницу каталога участников и метаданные фильтра."""

    roster = _base_roster()
    chosen_filter = http_request.GET.get('filter')
    viewer = http_request.user

    if not _should_filter(viewer, chosen_filter):
        return {
            'page_obj': slice_for_page(http_request, roster, MEMBER_PAGE_SIZE),
            'active_filter': '',
            'filter_options': CATALOG_FILTER_LABELS,
        }

    narrowed = _apply_catalog_filter(roster, viewer, chosen_filter)
    narrowed = narrowed.exclude(pk=viewer.pk).distinct()

    return {
        'page_obj': slice_for_page(http_request, narrowed, MEMBER_PAGE_SIZE),
        'active_filter': chosen_filter,
        'filter_options': CATALOG_FILTER_LABELS,
    }
