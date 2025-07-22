from django import forms
from .models import Producto, Ubicacion, Pallet, RemitoSalida, DetalleSalida
from django.forms import inlineformset_factory

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['pallet', 'codigo_barras', 'nombre', 'cantidad']
        widgets = {
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': 'Escaneá o ingresá el código',
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'pallet': forms.Select(attrs={'class': 'form-select'}),
        }


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la ubicación'})
        }

class PalletForm(forms.ModelForm):
    class Meta:
        model = Pallet
        fields = ['numero_pallet', 'ubicacion']
        widgets = {
            'numero_pallet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de pallet'}),
            'ubicacion': forms.Select(attrs={'class': 'form-select'}),
        }


class RemitoSalidaForm(forms.ModelForm):
    class Meta:
        model = RemitoSalida
        fields = ['destino', 'observaciones']
        widgets = {
            'destino': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Destino del remito'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
        }

class DetalleSalidaForm(forms.ModelForm):
    class Meta:
        model = DetalleSalida
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Cantidad a retirar'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar productos con stock disponible
        self.fields['producto'].queryset = Producto.objects.filter(cantidad__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        if producto and cantidad:
            if cantidad > producto.cantidad:
                raise forms.ValidationError(
                    f'Stock insuficiente para {producto.nombre}. '
                    f'Stock disponible: {producto.cantidad}'
                )
        return cleaned_data

# Formset para manejar múltiples detalles en un remito
DetalleSalidaFormSet = inlineformset_factory(
    RemitoSalida,
    DetalleSalida,
    form=DetalleSalidaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)