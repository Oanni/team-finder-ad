from projects.models import Project


def _with_relations():
    return (
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
    )


def newest_first(queryset):
    return queryset.order_by('-created_at', '-id')


def catalog_queryset():
    """Все проекты для главной страницы."""

    return newest_first(_with_relations())


def bookmarked_by(member):
    """Избранные проекты конкретного участника."""

    return newest_first(member.favorites.select_related('owner').prefetch_related('participants'))
