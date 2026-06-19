import re

from django import forms
from django.contrib.auth import get_user_model

from users.identifiers import (
    COUNTRY_DIGIT_COUNT,
    LEGACY_PREFIX,
    LOCAL_DIGIT_COUNT,
    UNIFIED_PREFIX,
)

Member = get_user_model()


def _strip_to_digits(raw_value):
    return re.sub(r'\D', '', raw_value)


def _apply_country_code(digit_string):
    if (
        len(digit_string) == COUNTRY_DIGIT_COUNT
        and digit_string.startswith(LEGACY_PREFIX)
    ):
        return UNIFIED_PREFIX + digit_string[1:]
    if len(digit_string) == LOCAL_DIGIT_COUNT:
        return UNIFIED_PREFIX + digit_string
    return digit_string


def _collision_exists(canonical, editing_member):
    lookup = Member.objects.filter(phone=canonical)
    if editing_member and editing_member.pk:
        lookup = lookup.exclude(pk=editing_member.pk)
    return lookup.exists()


def normalize_mobile_number(raw_value, editing_member=None):
    """Приводит телефон к +7… и проверяет уникальность."""

    if not raw_value or not raw_value.strip():
        return None

    digits_only = _strip_to_digits(raw_value)
    acceptable_lengths = (LOCAL_DIGIT_COUNT, COUNTRY_DIGIT_COUNT)

    if len(digits_only) not in acceptable_lengths:
        raise forms.ValidationError(
            f'Номер телефона должен содержать {LOCAL_DIGIT_COUNT} или '
            f'{COUNTRY_DIGIT_COUNT} цифр'
        )

    with_prefix = _apply_country_code(digits_only)
    canonical = '+' + with_prefix

    if _collision_exists(canonical, editing_member):
        raise forms.ValidationError(
            'Пользователь с таким номером телефона уже существует'
        )

    return canonical


def assert_github_host(target_url):
    """Проверяет, что URL ведёт на github.com."""

    if not target_url:
        return target_url

    if 'github.com' not in target_url.lower():
        raise forms.ValidationError('Ссылка должна вести на GitHub')

    return target_url
