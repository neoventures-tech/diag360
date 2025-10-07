from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """
    Converte markdown simples em HTML
    Suporta: ### títulos, **negrito**, listas com -
    """
    if not text:
        return ""

    # Converter ### Títulos
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)

    # Converter **negrito**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # Converter listas com -
    lines = text.split('\n')
    in_list = False
    result_lines = []

    for line in lines:
        # Detectar item de lista
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            # Remover "- " e adicionar <li>
            item_text = line.strip()[2:]
            result_lines.append(f'<li>{item_text}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)

    # Fechar lista se ainda estiver aberta
    if in_list:
        result_lines.append('</ul>')

    text = '\n'.join(result_lines)

    # Converter quebras de linha duplas em parágrafos
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []

    for p in paragraphs:
        p = p.strip()
        if p:
            # Não adicionar <p> se já for um elemento HTML
            if not (p.startswith('<h3>') or p.startswith('<ul>') or p.startswith('</ul>')):
                p = f'<p>{p}</p>'
            formatted_paragraphs.append(p)

    text = '\n'.join(formatted_paragraphs)

    return mark_safe(text)
