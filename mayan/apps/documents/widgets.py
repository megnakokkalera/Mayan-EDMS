from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .settings import (
    setting_display_width, setting_display_height, setting_preview_width,
    setting_preview_height, setting_thumbnail_width, setting_thumbnail_height
)


class DocumentFilePageImageWidget(forms.widgets.Widget):
    template_name = 'documents/forms/widgets/document_file_page_image_interactive.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'rotation': 0,
            'zoom': 100,
            'width': setting_display_width.value,
            'height': setting_display_height.value,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value


class DocumentFilePagesCarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of a document's pages
    """
    template_name = 'documents/forms/widgets/document_file_page_carousel.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'height': setting_preview_height.value,
            'width': setting_preview_width.value,
            'target_view': 'documents:document_file_page_view',
        }

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value


class DocumentFilePageThumbnailWidget:
    def render(self, instance):
        return render_to_string(
            template_name='documents/widgets/document_thumbnail.html',
            context={
                # Disable the clickable link if the document is in the trash
                'disable_title_link': instance.is_in_trash,
                'gallery_name': 'document_list',
                'instance': instance,
                'size_preview_width': setting_preview_width.value,
                'size_preview_height': setting_preview_height.value,
                'size_thumbnail_width': setting_thumbnail_width.value,
                'size_thumbnail_height': setting_thumbnail_height.value,
            }
        )


class ThumbnailFormWidget(forms.widgets.Widget):
    def render(self, *args, **kwargs):
        instance = kwargs['value']
        if instance:
           context={
                # Disable the clickable link if the document is in the trash
                'disable_title_link': instance.is_in_trash,
                'gallery_name': 'document_list',
                'instance': instance,
                'size_preview_width': setting_preview_width.value,
                'size_preview_height': setting_preview_height.value,
                'size_thumbnail_width': 150,#setting_thumbnail_width.value,
                'size_thumbnail_height': setting_thumbnail_height.value,
            }
        else:
            context = {}
        return render_to_string(
            template_name='documents/widgets/document_thumbnail.html',
            context=context
        )


class DocumentVersionPagesCarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of a document's pages
    """
    template_name = 'documents/forms/widgets/document_file_page_carousel.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'height': setting_preview_height.value,
            'width': setting_preview_width.value,
            'target_view': 'documents:document_version_page_view',
        }

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value



#TODO: Same as DocumentFilePageImageWidget
class DocumentVersionPageImageWidget(forms.widgets.Widget):
    template_name = 'documents/forms/widgets/document_file_page_image_interactive.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'rotation': 0,
            'zoom': 100,
            'width': setting_display_width.value,
            'height': setting_display_height.value,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value


class DocumentVersionPageThumbnailWidget:
    def render(self, instance):
        return render_to_string(
            template_name='documents/widgets/document_thumbnail.html',
            context={
                # Disable the clickable link if the document is in the trash
                'disable_title_link': instance.is_in_trash,
                'gallery_name': 'document_list',
                'instance': instance,
                'size_preview_width': setting_preview_width.value,
                'size_preview_height': setting_preview_height.value,
                'size_thumbnail_width': setting_thumbnail_width.value,
                'size_thumbnail_height': setting_thumbnail_height.value,
            }
        )


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (
        document.get_absolute_url(), document)
    )


def widget_document_file_page_number(document_file):
    return mark_safe(s=_('Pages: %d') % document_file.pages.count())


def widget_document_page_number(document):
    return mark_safe(s=_('Pages: %d') % document.pages.count())


def widget_document_version_page_number(document_version):
    return mark_safe(s=_('Pages: %d') % document_version.pages.count())
