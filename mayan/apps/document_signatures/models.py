from __future__ import unicode_literals

import logging
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_gpg.runtime import gpg
from documents.models import DocumentVersion
from documents.runtime import storage_backend

from .managers import DocumentVersionSignatureManager

logger = logging.getLogger(__name__)


def upload_to(*args, **kwargs):
    return unicode(uuid.uuid4())


class DocumentVersionSignature(models.Model):
    """
    Model that describes a document version signature properties
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_('Document version'), editable=False)
    signature_file = models.FileField(blank=True, null=True, upload_to=upload_to, storage=storage_backend, verbose_name=_('Signature file'))
    has_embedded_signature = models.BooleanField(default=False, verbose_name=_('Has embedded signature'))

    objects = DocumentVersionSignatureManager()

    def delete_detached_signature_file(self):
        self.signature_file.storage.delete(self.signature_file.path)

    def check_for_embedded_signature(self):
        logger.debug('checking for embedded signature')

        with self.document_version.open(raw=True) as file_object:
            self.has_embedded_signature = gpg.has_embedded_signature(file_object)
            self.save()

    class Meta:
        verbose_name = _('Document version signature')
        verbose_name_plural = _('Document version signatures')
