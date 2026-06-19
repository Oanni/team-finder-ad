from django.contrib.auth.models import BaseUserManager


class AccountLifecycleManager(BaseUserManager):
    """Фабрика учётных записей платформы."""

    def _assert_required(self, mailbox, given_name, family_name):
        if not mailbox:
            raise ValueError('Укажите email')
        if not given_name:
            raise ValueError('Укажите ваше имя')
        if not family_name:
            raise ValueError('Укажите вашу фамилию')

    def _spawn_record(self, mailbox, given_name, family_name, handset, secret, flags):
        record = self.model(
            email=mailbox,
            name=given_name,
            surname=family_name,
            phone=handset,
            **flags,
        )
        record.set_password(secret)
        record.save(using=self._db)
        return record

    def create_user(
        self,
        email,
        name,
        surname,
        phone=None,
        password=None,
        **extras
    ):
        self._assert_required(email, name, surname)
        mailbox = self.normalize_email(email)
        return self._spawn_record(mailbox, name, surname, phone, password, extras)

    def create_superuser(
        self,
        email,
        name,
        surname,
        phone=None,
        password=None,
        **extras
    ):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)
        return self.create_user(
            email, name, surname, phone, password, **extras
        )
