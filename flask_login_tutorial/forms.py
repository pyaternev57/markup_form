from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .utils import get_data


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    # email = StringField(
    #     'Email',
    #     validators=[
    #         Length(min=6),
    #         Email(message='Enter a valid email.'),
    #         DataRequired()
    #     ]
    # )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    # website = StringField(
    #     'Website',
    #     validators=[Optional()]
    # )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class DataForm(FlaskForm):
    data = get_data()
    data_format = SelectField("data_format", 
                        choices=[
                            "None", 
                            "Table",
                            "Audio",
                            "Image",
                            "Text",
                            "Time Series"
                            ])
    graph_vertex = SelectField(
        "graph_vertex", choices=list(data.keys())
    )
    graph_vertex_subclass = StringField(
        "graph_vertex_subclass", [DataRequired()],
    )
    errors_in_chunk = SelectField("errors", choices=["No", "Yes"])
    mark = SelectField("marks", choices=[
        (5, "идеально соответствует"),
        (4, "почти соответствует"),
        (3, "скорее соттвествует"),
        (2, "скорее не соттвествует"),
        (1, "почти не соответствует")])
    back = SubmitField("back")
    forward = SubmitField("next")


    def validate_graph_vertex_subclass(form, field):
        if field.data not in form.data[form.graph_vertex.data]:
            raise ValidationError('Please check filed ')