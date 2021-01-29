from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from car_park.models import Opinion, SavedUserCarPark, Category


class AddCarParkForm(forms.Form):
    """
    A form that creates a car park.
    Checks if car park is free, there is no price data and vice versa.
    Check whether the car park has a specific location.
    """
    spot_name = forms.CharField(label='Miejscowość', min_length=2, max_length=100, required=False)
    street = forms.CharField(label='Ulica', min_length=2, max_length=100, required=False)
    street.widget.attrs.update(placeholder='pole nie jest wymagane')
    street_number = forms.IntegerField(label='Numer', widget=forms.TextInput, required=False)
    name = forms.CharField(label='Nazwa parkingu', min_length=2, max_length=100)
    description = forms.CharField(label='Opis', required=False,
                                  widget=forms.Textarea(attrs={'cols': 21, 'placeholder': 'pole nie jest wymagane'}))
    longitude = forms.CharField(widget=forms.HiddenInput())
    latitude = forms.CharField(widget=forms.HiddenInput())
    categories = forms.ModelMultipleChoiceField(label='Kategorie',
                                                queryset=Category.objects.all().order_by('name'),
                                                required=False,
                                                widget=forms.CheckboxSelectMultiple)
    free_of_charge = forms.BooleanField(label='Czy parking jest bezpłatny', required=False)
    tariffs_name = forms.CharField(label='Nazwa taryfy', required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'pole nie jest wymagane'}))
    first_hour_fee = forms.DecimalField(label='Opłata za pierwszą godzinę postoju', max_digits=5, decimal_places=2,
                                        min_value=0, required=False)
    maximum_additional_fee = forms.DecimalField(label='Maksymalna opłata dodatkowa', max_digits=5, decimal_places=2,
                                                min_value=0, required=False)
    additional_fee_description = forms.CharField(label='Opis maksymalnej dopłaty', required=False,
                                                 widget=forms.Textarea(attrs={'cols': 21}))

    def clean(self):
        cleaned_data = super().clean()
        free_of_charge = cleaned_data.get('free_of_charge')
        first_hour_fee = cleaned_data.get('first_hour_fee')
        maximum_additional_fee = cleaned_data.get('maximum_additional_fee')
        additional_fee_description = cleaned_data.get('additional_fee_description')
        longitude = cleaned_data.get('longitude')
        latitude = cleaned_data.get('latitude')
        if free_of_charge and (first_hour_fee or maximum_additional_fee or additional_fee_description):
            raise forms.ValidationError(
                'Nie zaznaczaj pola "Czy jest bezpłatny" '
                'razem z wypełnionym polem dotyczącym opłat'
            )
        if not free_of_charge and not any([first_hour_fee, maximum_additional_fee, additional_fee_description]):
            raise forms.ValidationError(
                'Proszę wypełnij przynajmniej jedno z czterech pól dotyczących opłaty'
            )
        if not longitude or not latitude:
            raise forms.ValidationError('Nie można dodać parkingu bez jego lokalizacji')
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username,
    password, first_name, last_name and email.
    """
    username = forms.CharField(label='Nazwa użytkownika')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email",)


class EditProfileForm(forms.ModelForm):
    """A form for changing user data."""
    username = forms.CharField(label='Nazwa użytkownika')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    Check if the new password is different from the old one.
    """
    new_password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if old_password == new_password1 or old_password == new_password2:
            raise forms.ValidationError('Nowe hasło musi się różnić od starego')
        return cleaned_data


class SearchForm(forms.Form):
    """Car park search form."""
    spot_name = forms.CharField(label='Miejscowość', min_length=2, max_length=100, required=False)
    street = forms.CharField(label='Ulica', min_length=2, max_length=100, required=False)
    street_number = forms.IntegerField(label='Numer', widget=forms.TextInput, required=False)
    name = forms.CharField(label='Nazwa parkingu', min_length=2, max_length=100, required=False)
    longitude = forms.CharField(widget=forms.HiddenInput(), required=False)
    latitude = forms.CharField(widget=forms.HiddenInput(), required=False)
    free_of_charge = forms.BooleanField(label='Szukaj tylko bezpłatnych parkingów', required=False)
    tariffs_name = forms.CharField(label='Nazwa taryfy', required=False)
    first_hour_fee_from = forms.DecimalField(label='Opłata za pierwszą godzinę postoju OD', max_digits=5,
                                             decimal_places=2,
                                             min_value=0, required=False,
                                             widget=forms.TextInput(attrs={'type': 'range'}))
    first_hour_fee_to = forms.DecimalField(label='Opłata za pierwszą godzinę postoju DO', max_digits=5,
                                           decimal_places=2,
                                           min_value=0, required=False,
                                           widget=forms.TextInput(attrs={'type': 'range'}))
    maximum_additional_fee = forms.DecimalField(label='Maksymalna opłata dodatkowa', max_digits=5, decimal_places=2,
                                                min_value=0, required=False,
                                                widget=forms.TextInput(attrs={'type': 'range'}))

    def clean(self):
        cleaned_data = super().clean()
        first_hour_fee_from = cleaned_data.get('first_hour_fee_from')
        first_hour_fee_to = cleaned_data.get('first_hour_fee_to')
        if first_hour_fee_from > first_hour_fee_to:
            raise forms.ValidationError('Opłata "OD" musi być większa od opłaty "DO"')
        return cleaned_data


class OpinionForm(forms.Form):
    """A form for adding opinions about the car park."""
    YES_NO_CHOICES = (
        (0, 'Nie'),
        (1, 'Tak'),
    )
    opinion = forms.CharField(label='Opinia', min_length=2, max_length=250, widget=forms.Textarea)
    stars = forms.ChoiceField(label='Ile gwiazdek', choices=Opinion.STARS_CHOICES, widget=forms.RadioSelect)
    recommendation = forms.ChoiceField(label='Czy polecasz', choices=YES_NO_CHOICES, widget=forms.RadioSelect)


class OpinionDeleteForm(forms.ModelForm):
    """A form to delete an opinion."""

    class Meta:
        model = Opinion
        fields = []


class SavedUserCarParkForm(forms.ModelForm):
    """A form that allows user to add a car park to the user's saved car parks."""

    class Meta:
        model = SavedUserCarPark
        fields = ('notes',)
