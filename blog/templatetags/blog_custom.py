from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension
from django.shortcuts import resolve_url
from urllib import parse


register = template.Library()

# next prev pagenation
@register.simple_tag
def url_replace(request, field, value):

    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()

# 動的リンク
@register.simple_tag
def get_return_link(request):

    top_page = resolve_url('blog:public_list')
    referer = request.environ.get('HTTP_REFERER')

    if referer:
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer

    return top_page


@register.filter
def markdown_to_html(text):

    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)


class EscapeHtml(Extension):

    def extendMarkdown(self, md):

        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):

    extensions = settings.MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)
