from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

from users.identifiers import PHONE_MAX_LENGTH, SECRET_MIN_LEN
from users.portrait import build_initial_portrait
from users.validators import assert_github_host, normalize_mobile_number

Member = get_user_model()


class NewMemberForm(forms.ModelForm):
    """Регистрация нового участника."""

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Member
        fields = ("name", "surname", "email", "password")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "email": "Email",
        }

    def _reject_duplicate_mailbox(self, mailbox):
        if Member.objects.filter(email=mailbox).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует'
            )

    def clean_email(self):
        mailbox = self.cleaned_data.get('email')
        self._reject_duplicate_mailbox(mailbox)
        return mailbox

    def _attach_portrait(self, record):
        if record.avatar:
            return
        portrait_file = build_initial_portrait(record)
        record.avatar.save(portrait_file.name, portrait_file, save=True)

    def save(self, commit=True):
        record = super().save(commit=False)
        record.set_password(self.cleaned_data["password"])

        if not commit:
            return record

        record.save()
        self._attach_portrait(record)
        return record


class SecretRotationForm(forms.Form):
    """Смена пароля текущего участника."""

    old_password = forms.CharField(
        label="Текущий пароль",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите старый пароль'}
        ),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Минимум 8 символов'}),
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите еще раз'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        prior_secret = self.cleaned_data.get('old_password')
        if not self.user.check_password(prior_secret):
            raise forms.ValidationError('Неверный действующий пароль')
        return prior_secret

    def clean_new_password1(self):
        fresh_secret = self.cleaned_data.get('new_password1')
        if fresh_secret and len(fresh_secret) < SECRET_MIN_LEN:
            raise forms.ValidationError(
                f'Пароль должен содержать минимум {SECRET_MIN_LEN} символов'
            )
        return fresh_secret

    def _assert_secrets_match(self, first, second):
        if first and second and first != second:
            raise forms.ValidationError('Пароли не совпадают')

    def clean(self):
        payload = super().clean()
        self._assert_secrets_match(
            payload.get('new_password1'),
            payload.get('new_password2'),
        )
        return payload

    def save(self):
        rotated = self.cleaned_data.get('new_password1')
        self.user.set_password(rotated)
        self.user.save()
        return self.user


class CredentialChallengeForm(forms.Form):
    """Проверка email и пароля при входе."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def _locate_account(self, mailbox):
        return Member.objects.filter(email=mailbox).first()

    def _bind_session_user(self, mailbox, secret):
        return authenticate(
            request=self.request,
            username=mailbox,
            password=secret,
        )

    def clean(self):
        payload = super().clean()
        mailbox = payload.get('email')
        secret = payload.get('password')

        if not (mailbox and secret):
            return payload

        account = self._locate_account(mailbox)
        if account is None:
            raise ValidationError('Неверный email или пароль')

        session_user = self._bind_session_user(account.email, secret)
        if session_user is None:
            raise ValidationError('Неверный email или пароль')

        if not session_user.is_active:
            raise ValidationError('Учётная запись не активна')

        self.user = session_user
        return payload

    def get_user(self):
        return self.user


class MemberProfileForm(forms.ModelForm):
    """Редактирование визитки участника."""

    phone = forms.CharField(
        max_length=PHONE_MAX_LENGTH,
        label="Контактный телефон",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '+7XXXXXXXXXX или 8XXXXXXXXXX'}
        ),
    )

    github_url = forms.URLField(
        required=False,
        label="Профиль GitHub",
        widget=forms.URLInput(
            attrs={'placeholder': 'https://github.com/username'}
        ),
    )

    class Meta:
        model = Member
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'avatar': 'Аватар',
            'about': 'О себе',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'surname': forms.TextInput(
                attrs={'placeholder': 'Введите фамилию'}
            ),
            'avatar': forms.FileInput(),
            'about': forms.Textarea(
                attrs={'placeholder': 'Расскажите о себе', 'rows': 4}
            ),
        }

    def clean_phone(self):
        handset = self.cleaned_data.get('phone')
        return normalize_mobile_number(handset, editing_member=self.instance)

    def clean_github_url(self):
        link = self.cleaned_data.get('github_url')
        return assert_github_host(link)
