from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import (UserLoginSerializer, UserRegisterSerializer,
                          UserVerifySerializer, ResendVerifyMessageSerializer,
                          RefreshTokenSerializer, TokenSerializer, UserVerifyResponseSerializer,
                          AccessTokenSerializer, )
from .services import (user_login_func, user_register_func, user_verify_func,
                       user_resend_func, refresh_token_func, check_verify_token_func,
                       user_logout_func,)
from apps.api.response import base_response, base_response_with_validation_error, base_response_with_error
from apps.api import response_code


class UserLoginView(APIView):
    """
    The login function is the function that should do this:
        1. Get user information for login (such as email).
        2. Login the user or send a message confirming the account

        return:
            if user verify by password, return a Dictionary included(User Info, Tokens)
            if user verify by code or uuid, return None
        Note:
            If registration is done only with (mobile number or email), then login and register are done in one view
             and function.
    """
    serializer_class = UserLoginSerializer

    @extend_schema(request=UserLoginSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_login_func(request=request, phone_number=serializer.validated_data['phone_number'])
            except PermissionError:
                return base_response_with_error(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                                success=False, code=response_code.TOO_MANY_REQUEST_OTP_CODE)
            return base_response(status_code=status.HTTP_200_OK, success=True, code=response_code.OK)

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)


class UserRegisterView(APIView):
    """
    The register function is the function that should do this:
        1. Get user information for register (such as phone number, email, password)
        2. send a message confirming the account

        return:
            return None
    """
    serializer_class = UserRegisterSerializer

    @extend_schema(request=UserRegisterSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                user_register_func(request=request, phone_number=vd['phone_number'], fullname=vd['fullname'])
            except PermissionError:
                return base_response_with_error(status_code=status.HTTP_429_TOO_MANY_REQUESTS, success=False,
                                                code=response_code.TOO_MANY_REQUEST_OTP_CODE)
            return base_response(status_code=status.HTTP_200_OK, success=True, code=response_code.OK)

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)


class UserVerifyView(APIView):
    """
    The verify function is the function that should be this:
        1. Get otp code or uuid
        2, verifying account

        return:
            return User info and Tokens
    """
    serializer_class = UserVerifySerializer

    @extend_schema(request=UserVerifySerializer, responses=UserVerifyResponseSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                data = user_verify_func(request=request, code=vd['code'], phone_number=vd['phone_number'])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE, success=False,
                                                code=response_code.INVALID_OTP)
            return base_response(status_code=status.HTTP_200_OK, success=True, code=response_code.OK, result=data)

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)


class ResendVerifyMessage(APIView):
    """
    The resend verify message function is the function that should do this:
        1. Get Email or Phone number
        2. Check validate to resend verify message, else raise Exception
        3. send message

        return:
            return None
    """
    serializer_class = ResendVerifyMessageSerializer

    @extend_schema(request=ResendVerifyMessageSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_resend_func(request=request, phone_number=serializer.validated_data['phone_number'])
            except PermissionError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE, success=False,
                                                code=response_code.INVALID_OTP)
            return base_response(status_code=status.HTTP_200_OK, success=True, code=response_code.OK)

        return base_response_with_validation_error(
            status_code=status.HTTP_400_BAD_REQUEST, success=False,
            code=response_code.BAD_REQUEST, error=serializer.errors)


class JwtRefreshView(APIView):
    """
    The refresh token function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid. return Access token, else raise Exception

        return:
            Access Token
    """
    serializer_class = RefreshTokenSerializer

    @extend_schema(request=RefreshTokenSerializer, responses=AccessTokenSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                access_token = refresh_token_func(
                    request=request,
                    encrypted_refresh_token=serializer.validated_data['refresh_token'])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                success=False, code=response_code.INVALID_REFRESH_TOKEN)
            return base_response(status_code=status.HTTP_200_OK, success=True,
                                 code=response_code.OK, result={"access_token": access_token})

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)


class JwtVerifyView(APIView):
    """
    The jwt verify function is the function that should do this:
        1. Get Token.
        2. if token is valid. return True, else return False.
    """
    serializer_class = TokenSerializer

    @extend_schema(request=TokenSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            check = check_verify_token_func(
                request=request, encrypted_token=serializer.validated_data['token'])
            if check is False:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                success=False, code=response_code.INVALID_TOKEN)
            return base_response(status_code=status.HTTP_200_OK, success=True, code=response_code.OK)

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)


class UserLogoutView(APIView):
    """
    The logout function is the function that should do this:
        1. Get Refresh token.
        2. check validate refresh token
        3. if refresh token is valid, it will be blacklisted. else raise Exception

        return:
            return None
    """
    serializer_class = TokenSerializer

    @extend_schema(request=RefreshTokenSerializer, responses=None)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_logout_func(request=request, encrypted_token=serializer.validated_data['token'])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                success=False, code=response_code.INVALID_TOKEN)
            return base_response(status_code=status.HTTP_204_NO_CONTENT, success=True, code=response_code.NO_CONTENT)

        return base_response_with_validation_error(status_code=status.HTTP_400_BAD_REQUEST, success=False,
                                                   code=response_code.BAD_REQUEST, error=serializer.errors)
