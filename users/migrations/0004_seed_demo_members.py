from django.contrib.auth.hashers import make_password
from django.db import migrations

DEMO_SECRET = 'crewlink2026'

ROSTER = [
    {
        'email': 'ibetu@crewlink.dev',
        'name': 'Алексей',
        'surname': 'Ибетуллов',
        'phone': '+79851112233',
        'about': 'Бэкенд, Django, pet-проекты.',
        'github_url': 'https://github.com/ibetu',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'sofia.m@crewlink.dev',
        'name': 'София',
        'surname': 'Морозова',
        'phone': '+79852223344',
        'about': 'UI/UX и фронтенд. Люблю аккуратные интерфейсы.',
        'github_url': 'https://github.com/sofia-morozova',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'artyom.k@crewlink.dev',
        'name': 'Артём',
        'surname': 'Климов',
        'phone': '+79853334455',
        'about': 'DevOps и инфраструктура. Docker, CI/CD.',
        'github_url': 'https://github.com/artyom-klimov',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'ops@crewlink.dev',
        'name': 'Команда',
        'surname': 'Админ',
        'phone': '+79854445566',
        'about': 'Служебный аккаунт.',
        'is_staff': True,
        'is_superuser': True,
    },
]

ROSTER_EMAILS = [entry['email'] for entry in ROSTER]


def populate_demo_roster(apps, schema_editor):
    Member = apps.get_model('users', 'User')
    hashed = make_password(DEMO_SECRET)

    for profile in ROSTER:
        if Member.objects.filter(email=profile['email']).exists():
            continue
        Member.objects.create(
            password=hashed,
            is_active=True,
            **profile,
        )


def purge_demo_roster(apps, schema_editor):
    Member = apps.get_model('users', 'User')
    Member.objects.filter(email__in=ROSTER_EMAILS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_phone_nullable_unique'),
    ]

    operations = [
        migrations.RunPython(populate_demo_roster, purge_demo_roster),
    ]
