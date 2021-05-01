from flask_security.forms import RegisterForm, Required
from wtforms import StringField


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [Required()])

