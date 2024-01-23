from django.utils.translation import gettext_lazy as _

OK = 2000
NOT_ACCEPTABLE = 4060
BAD_REQUEST = 4010
TOO_MANY_REQUEST = 4290
TOO_MANY_REQUEST_OTP_CODE = 4291

INVALID_OTP = 4061

ERROR_TRANSLATION = {
    INVALID_OTP: _("Invalid code"),
    TOO_MANY_REQUEST: _("Please try again later"),
    TOO_MANY_REQUEST_OTP_CODE: _("You can only receive a otp code every two minutes")
}
