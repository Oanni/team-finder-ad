from django import forms

from projects.models import Project


def _strip_github_link(raw_link):
    if not raw_link:
        return raw_link
    return raw_link.strip()


def _points_to_github_host(link):
    return 'github.com' in link.lower()


class VentureDraftForm(forms.ModelForm):
    """Форма публикации или правки pet-проекта."""

    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'github_url': 'Ссылка на GitHub',
            'status': 'Статус',
        }
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Введите название'}),
            "description": forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Опишите проект',
            }),
        }

    def clean_github_url(self):
        link = _strip_github_link(self.cleaned_data.get('github_url'))

        if link and not _points_to_github_host(link):
            raise forms.ValidationError(
                'Ссылка должна вести на GitHub (github.com)'
            )

        return link
