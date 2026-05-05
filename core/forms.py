from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmployeeSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This adds the Tailwind styling to the actual boxes
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'appearance-none block w-full px-4 py-3 border border-slate-300 rounded-xl shadow-sm placeholder-slate-400 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm transition-all bg-slate-50/50'
            })
