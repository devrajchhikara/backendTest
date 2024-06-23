from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, UploadedFile

class FileManagementTests(APITestCase):

    def setUp(self):
        self.ops_user = User.objects.create_user(username='ops_user', password='password', is_ops_user=True)
        self.client_user = User.objects.create_user(username='client_user', password='password', is_client_user=True)
        self.client_user.is_active = True
        self.client_user.save()

    def test_ops_user_can_upload_file(self):
        self.client.login(username='ops_user', password='password')
        url = reverse('uploadedfile-upload-file')
        with open('test_file.docx', 'rb') as file:
            response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_user_can_list_files(self):
        self.client.login(username='client_user', password='password')
        url = reverse('uploadedfile-list-files')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_can_download_file(self):
        self.client.login(username='client_user', password='password')
        url = reverse('uploadedfile-download-file', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
