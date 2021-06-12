from rest_framework import generics, permissions, views, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.conf import settings
from random import randint
import os

from .serializers import CreateUserSerializers, UserSerializers, \
    ChangePasswordSerializer, GetMeSerializer, UpdateUserSerializers
from .models import User
from utils.send_letter_on_email.send_letter_on_email import Util
from utils.optimization_photo.optimization_photo import optimization_photo
from utils.format_images.format_images import check_uploaded_image_format
from utils.exception_handling.exception_views import base_view


class UserListView(generics.ListAPIView):
    """Get all users (GET)"""
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Getting user by param (GET)"""
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    """Create user (post)"""
    serializer_class = CreateUserSerializers
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class UserUpdateData(generics.UpdateAPIView):
    """Change data about me"""
    serializer_class = UpdateUserSerializers
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()

    @base_view
    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            path = 'images/' + str(request.user.photo)

            if data['first_name']:
                request.user.first_name = data['first_name']

            if data['sex']:
                request.user.sex = data['sex']

            if data['birth_day']:
                request.user.birth_day = data['birth_day']

            if data['city']:
                request.user.city = data['city']

            if data['photo']:
                result = check_uploaded_image_format(data['photo'])
                if result:
                    return result
                request.user.photo = data['photo']
                os.remove(path)

            request.user.save()

            if data['photo']:
                result = optimization_photo(
                    request.user,
                    message_success='Ваши данные успешно измененны',
                    message_error='Ошибка загруженного файла. Загрузите фотографию формата .jpg, .jpeg, .png',
                    json_response=True
                )

                return result

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Ваши данные успешно измененны',
                    'data': {
                        'id': request.user.pk,
                        'username': request.user.username,
                        'first_name': request.user.first_name,
                        'sex': request.user.sex,
                        'birth_day': request.user.birth_day,
                        'city': request.user.city,
                        'email': request.user.email,
                        'photo': settings.BASE_URL + 'images/' + str(request.user.photo),
                    }
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'При отправке данных произошла ошибка. '
                               'Передайте следующие параметры: '
                               'Имя пользователя, Город, День рождения, Пол, Фото'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(views.APIView):
    """Auth - register"""
    parser_classes = (MultiPartParser, FormParser,)

    @base_view
    def post(self, request):
        try:
            data = request.data
            checkEmail = User.objects.filter(email=data['email'])

            if checkEmail:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Данный E-Mail уже используется. Введите другой E-Mail, либо войдите в аккаунт'
                    },
                    status=400
                )

            if data['password'] != data['confirm_password']:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Пароли не совпадают!'
                    }, status=400
                )

            result = check_uploaded_image_format(data['photo'])
            if result:
                return result

            user = User.objects.create_user(
                data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                photo=data['photo'],
                city=data['city'],
                birth_day=data['birth_day'],
                sex=data['sex']
            )
            code = randint(123456, 987654)
            user.code_confirm = code

            user.save()

            # Optimization upload photo
            optimization_photo(
                user,
                message_success='Ваши данные успешно измененны',
                message_error='Ошибка загруженного файла. Загрузите фотографию формата .jpg, .jpeg, .png',
                json_response=False
            )

            del data['password']  # delete field password than they didn't get into the UI from data
            del data['confirm_password']  # delete field confirm_password that they didn't get the UI from data
            # Send letter to email
            email_body = 'Ваш код для подтверждения: ' + str(
                code) + '. Его следует использовать, чтобы подтвердить адрес электронной почты при регистрации.' + \
                         '\n\n' + f'Если вы {data["first_name"]} не запрашивали это сообщение, проигнорируйте его.' + '\n\n' + 'С уважением,' + '\n' + 'Команда VA'
            email_subject = 'Подтверждения вашего E-Mail'
            to_email = data['email']
            data_send_mail = {
                'email_body': email_body,
                'email_subject': email_subject,
                'to_email': to_email
            }
            Util.send_email(data=data_send_mail)

            return JsonResponse(
                {
                    'status': 'success'
                },
                status=201
            )
        except IntegrityError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Введенное имя пользователя уже используется. Введите другое имя пользователя'
                },
                status=400
            )


@base_view
@csrf_exempt
def verify_code(request):
    """Confirm Email ===> entering the code that came to the mail"""
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(code_confirm=int(data['code']))
        print('data ==> ', data)

        if user:
            user = User.objects.get(code_confirm=int(data['code']))
            user.confirm_email = True
            user.code_confirm = None
            user.save()
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'E-Mail успешно подтвержден'
                },
                status=200
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Введенный код неправильный'
                },
                status=400
            )


@base_view
@csrf_exempt
def forget_password(request):
    """Forget password"""
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(email=data['email'])
        if user:
            user = User.objects.get(email=data['email'])
            code = randint(123456, 987654)
            user.code_confirm = code
            user.save()
            # Send letter to email
            email_body = 'Ваш код: ' + str(
                code) + '. Его следует использовать, для восстановление доступа к вашему аккаунту.' + '\n\n' + \
                         f'Если Вы не запрашивали это сообщение, проигнорируйте его.' + '\n\n' + 'С уважением,' + '\n' + 'Команда VA'
            email_subject = 'Восстановление пароля'
            to_email = user.email
            data_send_mail = {
                'email_body': email_body,
                'email_subject': email_subject,
                'to_email': to_email
            }
            Util.send_email(data=data_send_mail)

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'На вашу почту отправленно письмо для восстановления аккаунта'
                },
                status=200
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'По вашему запросу ничего не найдено. Попробуйте ввести другой E-Mail.'
                },
                status=400
            )


@base_view
@csrf_exempt
def verify_forget_password(request):
    """Forget password ===> entering the code that came to the mail"""
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(code_confirm=int(data['code']))

        if user:
            user = User.objects.get(code_confirm=int(data['code']))
            user.code_confirm = None
            user.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Код успешно подтвержден'}, status=200
            )
        else:
            return JsonResponse(
                {'status': 'error', 'message': 'Введенный код неправильный'}, status=400
            )


@base_view
@csrf_exempt
def add_password_forget_password(request):
    """Forget password ===> enter new password"""
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.filter(email=data['email'])
        if user:
            if data['new_password'] == data['confirm_new_password']:
                user = User.objects.get(email=data['email'])
                user.password = data['new_password']
                user.save()
                return JsonResponse(
                    {
                        'status': 'success',
                        'message': 'Пароль успешно изменен'
                    },
                    status=200
                )
            else:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Введенные пароли не совпадают'
                    },
                    status=400
                )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Произошла ошибка. Попробуйте позже'
                },
                status=400
            )


class ChangePasswordView(generics.UpdateAPIView):
    """Auth - Change password ( into account )"""
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @base_view
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('self.object ===> ', self.object)
        serializer = self.get_serializer(data=request.data)
        print('serializer ===> ', serializer)

        if request.data['new_password'] != request.data['confirm_new_password']:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Пароли не совпадают'
                },
                status=200
            )


        if serializer.is_valid():
            # Checking old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return JsonResponse(
                    {
                        'status': 'error',
                        "message": "Неправильный пароль"
                    },
                    status=400
                )
            # set_password also hashes the password that the user will receive
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Пароль был успешно изменен'
                },
                status=200
            )
        return JsonResponse(
            {
                'status': 'error',
                'message': serializer.error
            },
            status=400
        )


class GetDataAboutMe(generics.ListAPIView):
    """Get data about me"""
    serializer_class = GetMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @base_view
    def get_queryset(self):
        print('self.request.user ==> ', self.request.user)
        print('self.request.user.username ==> ', self.request.user.username)
        user = User.objects.filter(username=self.request.user.username)
        return user
