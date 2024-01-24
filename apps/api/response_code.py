from django.utils.translation import gettext_lazy as _

OK = 2000
NO_CONTENT = 2040
NOT_ACCEPTABLE = 4060
BAD_REQUEST = 4010
TOO_MANY_REQUEST = 4290
TOO_MANY_REQUEST_OTP_CODE = 4291

INVALID_OTP = 4061
INVALID_REFRESH_TOKEN = 4062
INVALID_TOKEN = 4063

ERROR_TRANSLATION = {
    INVALID_OTP: _("Invalid code"),
    TOO_MANY_REQUEST: _("Please try again later"),
    TOO_MANY_REQUEST_OTP_CODE: _("You can only receive a otp code every two minutes"),
    INVALID_REFRESH_TOKEN: _("Invalid refresh token"),
    INVALID_TOKEN: _("Invalid token")
}
