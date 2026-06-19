from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.catalog import assemble_member_catalog
from users.forms import (
    CredentialChallengeForm,
    MemberProfileForm,
    NewMemberForm,
    SecretRotationForm,
)

Member = get_user_model()


def _render_signup_form(http_request, bound_form):
    return render(http_request, 'users/register.html', {'form': bound_form})


def _render_login_form(http_request, bound_form):
    return render(http_request, 'users/login.html', {'form': bound_form})


def enroll_new_member(http_request):
    """Регистрация и немедленный вход."""

    signup_form = NewMemberForm(data=http_request.POST or None)

    if signup_form.is_valid():
        fresh_member = signup_form.save()
        login(http_request, fresh_member)
        return redirect('projects:list')

    return _render_signup_form(http_request, signup_form)


def establish_session(http_request):
    """Аутентификация по email и паролю."""

    challenge = CredentialChallengeForm(
        request=http_request,
        data=http_request.POST or None,
    )

    if challenge.is_valid():
        login(http_request, challenge.get_user())
        return redirect('projects:list')

    return _render_login_form(http_request, challenge)


def terminate_session(http_request):
    """Завершение сессии и возврат на каталог проектов."""

    logout(http_request)
    return redirect('projects:list')


def _fetch_owned_ventures(member):
    return (
        member.owned_projects
        .select_related('owner')
        .order_by('-created_at')
    )


def display_member_card(http_request, pk):
    """Публичная визитка участника."""

    subject = get_object_or_404(Member, pk=pk)
    context = {
        'user': subject,
        'user_projects': _fetch_owned_ventures(subject),
    }
    return render(http_request, 'users/user-details.html', context)


def _profile_form_for_get(actor):
    return MemberProfileForm(instance=actor)


def _profile_form_for_post(actor, http_request):
    return MemberProfileForm(
        http_request.POST,
        http_request.FILES,
        instance=actor,
    )


@login_required
def revise_member_profile(http_request):
    """Обновление личных данных владельца профиля."""

    actor = http_request.user

    if http_request.method != 'POST':
        draft = _profile_form_for_get(actor)
        return render(
            http_request,
            'users/edit_profile.html',
            {'form': draft},
        )

    submission = _profile_form_for_post(actor, http_request)

    if submission.is_valid():
        submission.save()
        return redirect('users:profile', pk=actor.pk)

    return render(
        http_request,
        'users/edit_profile.html',
        {'form': submission},
    )


def browse_members(http_request):
    """Каталог участников с опциональной фильтрацией."""

    context = assemble_member_catalog(http_request)
    return render(http_request, 'users/participants.html', context)


def _empty_secret_form(actor):
    return SecretRotationForm(user=actor)


def _bound_secret_form(actor, http_request):
    return SecretRotationForm(user=actor, data=http_request.POST)


@login_required
def rotate_credentials(http_request):
    """Смена пароля авторизованного участника."""

    actor = http_request.user

    if http_request.method != 'POST':
        return render(
            http_request,
            'users/change_password.html',
            {'form': _empty_secret_form(actor)},
        )

    submission = _bound_secret_form(actor, http_request)

    if submission.is_valid():
        refreshed = submission.save()
        update_session_auth_hash(http_request, refreshed)
        return redirect('users:profile', pk=actor.pk)

    return render(
        http_request,
        'users/change_password.html',
        {'form': submission},
    )
