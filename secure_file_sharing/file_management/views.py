from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from .models import UploadedFile
from .serializers import UserSerializer, UploadedFileSerializer
from .permissions import IsOpsUser, IsClientUser
import os
from cryptography.fernet import Fernet

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_url = self.generate_verification_url(user)
            send_mail(
                'Verify your email',
                f'Please click the following link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            return Response({'message': 'User created, verification email sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='verify-email')
    def verify_email(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def generate_verification_url(self, user):
        # Generate a URL to verify email (implementation depends on your setup)
        pass

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'upload_file':
            self.permission_classes = [IsAuthenticated, IsOpsUser]
        elif self.action in ['list_files', 'download_file']:
            self.permission_classes = [IsAuthenticated, IsClientUser]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='upload-file')
    def upload_file(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        if not file.name.endswith(('pptx', 'docx', 'xlsx')):
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        uploaded_file = UploadedFile.objects.create(user=request.user, file=file)
        return Response(UploadedFileSerializer(uploaded_file).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='list-files')
    def list_files(self, request):
        files = UploadedFile.objects.all()
        return Response(UploadedFileSerializer(files, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='download-file/(?P<file_id>[^/.]+)')
    def download_file(self, request, file_id=None):
        try:
            file = UploadedFile.objects.get(id=file_id)
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_client_user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        file_path = file.file.path
        encrypted_url = self.generate_encrypted_url(file_path)
        return Response({'download-link': encrypted_url, 'message': 'success'}, status=status.HTTP_200_OK)

    def generate_encrypted_url(self, file_path):
        key = settings.ENCRYPTION_KEY
        fernet = Fernet(key)
        encrypted_path = fernet.encrypt(file_path.encode())
        return encrypted_path.decode()

    @action(detail=False, methods=['get'], url_path='download-file-by-url')
    def download_file_by_url(self, request):
        encrypted_url = request.query_params.get('url')
        if not encrypted_url:
            return Response({'error': 'No URL provided'}, status=status.HTTP_400_BAD_REQUEST)

        key = settings.ENCRYPTION_KEY
        fernet = Fernet(key)
        try:
            decrypted_path = fernet.decrypt(encrypted_url.encode()).decode()
        except:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

        if not os.path.exists(decrypted_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        with open(decrypted_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(decrypted_path)}'
            return response
