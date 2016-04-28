from django.forms import ModelForm, RadioSelect


class BirthNoteAdminForm(ModelForm):
    class Meta:
        widgets = {
            'child_gender': RadioSelect,
        }


class PersonAdminForm(ModelForm):
    class Meta:
        widgets = {
            'gender': RadioSelect,
        }
