from django.db import migrations

VENTURE_CATALOG = [
    {
        'name': 'Проект 1',
        'owner_email': 'ibetu@crewlink.dev',
        'description': 'Первый демо-проект.',
        'github_url': 'https://github.com/ibetu/project-1',
        'status': 'open',
    },
    {
        'name': 'Проект 2',
        'owner_email': 'sofia.m@crewlink.dev',
        'description': 'Второй демо-проект.',
        'github_url': 'https://github.com/sofia-morozova/project-2',
        'status': 'open',
    },
    {
        'name': 'Проект 3',
        'owner_email': 'ibetu@crewlink.dev',
        'description': 'Третий демо-проект (закрыт).',
        'status': 'closed',
    },
]

VENTURE_TITLES = [item['name'] for item in VENTURE_CATALOG]

LEGACY_TITLES = [
    'CrewLink — каталог идей',
    'Palette — UI-kit для стартапов',
    'Архив: прототип v0.3',
]


def _resolve_owner(Member, mailbox):
    try:
        return Member.objects.get(email=mailbox)
    except Member.DoesNotExist:
        return None


def populate_demo_ventures(apps, schema_editor):
    Member = apps.get_model('users', 'User')
    Venture = apps.get_model('projects', 'Project')

    Venture.objects.filter(name__in=LEGACY_TITLES).delete()

    for blueprint in VENTURE_CATALOG:
        author = _resolve_owner(Member, blueprint['owner_email'])
        if author is None:
            continue

        venture, created = Venture.objects.get_or_create(
            name=blueprint['name'],
            defaults={
                'description': blueprint['description'],
                'owner': author,
                'github_url': blueprint.get('github_url', ''),
                'status': blueprint['status'],
            },
        )

        if created:
            venture.participants.add(author)


def purge_demo_ventures(apps, schema_editor):
    Venture = apps.get_model('projects', 'Project')
    Venture.objects.filter(name__in=VENTURE_TITLES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_wire_venture_relations'),
        ('users', '0004_seed_demo_members'),
    ]

    operations = [
        migrations.RunPython(populate_demo_ventures, purge_demo_ventures),
    ]
