from django import template
from django.forms import CheckboxInput, Select

register = template.Library()


@register.filter
def bootstrap_field(field):
    widget = field.field.widget
    css_class = ('form-check-input' if isinstance(widget, CheckboxInput)
                 else 'form-select' if isinstance(widget, Select)
                 else 'form-control')
    attrs = {'class': f"{widget.attrs.get('class', '')} {css_class}".strip()}
    described_by = []
    if field.help_text:
        described_by.append(f'{field.auto_id}_helptext')
    if field.errors:
        attrs['class'] += ' is-invalid'
        attrs['aria-invalid'] = 'true'
        described_by.append(f'{field.auto_id}_errors')
    if described_by:
        attrs['aria-describedby'] = ' '.join(described_by)
    return field.as_widget(attrs=attrs)
