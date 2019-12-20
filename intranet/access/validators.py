from django.core.exceptions import ValidationError
from validate_docbr import CPF

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Telefone deve conter apenas números', 'digits')

    if len(value) > 11:
        raise ValidationError('Telefone deve ter no máximo 11 digitos', 'length')


def validate_period(period_from, period_to):
    if (period_from and period_to) and (period_from > period_to):
        raise ValidationError('A Data de início deve ser menor do que a Data de término')


def validate_doc_number(form, doc_type, doc_number):
    if doc_type == 'RG' and len(doc_number) != 9:
        error = ValidationError('RG deve ter 9 digitos', 'length')
        form.add_error('doc_number', error)

    if doc_type == 'CPF' and not _cpf_is_valid(doc_number):
        error = ValidationError('CPF é invalido', 'cpf')
        form.add_error('doc_number', error)


def _cpf_is_valid(cpf_number):
    cpf = CPF()
    return cpf.validate(cpf_number)

    