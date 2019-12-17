from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Telefone deve conter apenas números', 'digits')

    if len(value) > 11:
        raise ValidationError('Telefone deve ter no máximo 11 digitos', 'length')