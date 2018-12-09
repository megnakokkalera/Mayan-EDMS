from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import SmartLink
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import (
    TEST_SMART_LINK_DYNAMIC_LABEL, TEST_SMART_LINK_LABEL,
    TEST_SMART_LINK_LABEL_EDITED
)


class SmartLinkViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(SmartLinkViewTestCase, self).setUp()
        self.login_user()

    def test_smart_link_create_view_no_permission(self):
        response = self.post(
            'linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }
        )

        self.assertEquals(response.status_code, 403)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_create_view_with_permission(self):
        self.role.permissions.add(
            permission_smart_link_create.stored_permission
        )

        response = self.post(
            'linking:smart_link_create', data={
                'label': TEST_SMART_LINK_LABEL
            }, follow=True
        )
        self.assertContains(response, text='created', status_code=200)
        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(
            SmartLink.objects.first().label, TEST_SMART_LINK_LABEL
        )

    def test_smart_link_delete_view_no_permission(self):
        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_delete', args=(smart_link.pk,)
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(SmartLink.objects.count(), 1)

    def test_smart_link_delete_view_with_permission(self):
        self.role.permissions.add(
            permission_smart_link_delete.stored_permission
        )

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_delete', args=(smart_link.pk,), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(SmartLink.objects.count(), 0)

    def test_smart_link_edit_view_no_permission(self):
        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_edit', args=(smart_link.pk,), data={
                'label': TEST_SMART_LINK_LABEL_EDITED
            }
        )
        self.assertEqual(response.status_code, 403)
        smart_link = SmartLink.objects.get(pk=smart_link.pk)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL)

    def test_smart_link_edit_view_with_permission(self):
        self.role.permissions.add(
            permission_smart_link_edit.stored_permission
        )

        smart_link = SmartLink.objects.create(label=TEST_SMART_LINK_LABEL)

        response = self.post(
            'linking:smart_link_edit', args=(smart_link.pk,), data={
                'label': TEST_SMART_LINK_LABEL_EDITED
            }, follow=True
        )

        smart_link = SmartLink.objects.get(pk=smart_link.pk)
        self.assertContains(response, text='update', status_code=200)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL_EDITED)


class SmartLinkDocumentsViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(SmartLinkDocumentsViewTestCase, self).setUp()
        self.login_user()

    def setup_smart_links(self):
        smart_link = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        smart_link.document_types.add(self.document_type)

        smart_link_2 = SmartLink.objects.create(
            label=TEST_SMART_LINK_LABEL,
            dynamic_label=TEST_SMART_LINK_DYNAMIC_LABEL
        )
        smart_link_2.document_types.add(self.document_type)

    def test_document_smart_link_list_view_no_permission(self):
        self.setup_smart_links()

        self.role.permissions.add(
            permission_document_view.stored_permission
        )

        response = self.get(
            'linking:smart_link_instances_for_document',
            args=(self.document.pk,)
        )
        # Text must appear 2 times, only for the windows title and template
        # heading. The two smart links are not shown.

        self.assertContains(
            response, text=self.document.label, count=2, status_code=200
        )

    def test_document_smart_link_list_view_with_permission(self):
        self.setup_smart_links()

        self.role.permissions.add(
            permission_smart_link_view.stored_permission
        )

        self.role.permissions.add(
            permission_document_view.stored_permission
        )

        response = self.get(
            'linking:smart_link_instances_for_document',
            args=(self.document.pk,)
        )

        # Text must appear 4 times: 2 for the windows title and template
        # heading, plus 2 for the test.

        self.assertContains(
            response, text=self.document.label, count=4, status_code=200
        )
