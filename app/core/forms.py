from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .utils import get_data
from sqlalchemy import distinct
from .models import Graph, db


class AddVertex(FlaskForm):
    """"Updating graph with different choices
    add -> change all
    add_one_vertex -> add one new vertex
    """
    add = FileField("Update whole graph")
    graph_vertex = SelectField(
        "Choose a vertex class", choices=[el[0] for el in db.session.query(distinct(Graph.graph_vertex)).all()]
    )
    add_one_vertex = StringField("New vertex")
    submit = SubmitField('Submit')


# TODO change to read from google sheets
class AddNotebooks(FlaskForm):
    """"Updating list of notebooks"""
    add = FileField("csv with notebooks", validators=[DataRequired()])
    submit = SubmitField('Submit')


class StartPage(FlaskForm):
    add_vertexes = SubmitField('Add vertexes')
    add_notebooks = SubmitField('Add notebooks')
    markup_tool = SubmitField('Markup Tool')
    dashboard = SubmitField("Dashboard")

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
    # graph_vertex_subclass = StringField(
    #     "graph_vertex_subclass", [DataRequired()],
    # )
    graph_vertex_subclass = SelectField(
        "graph_vertex_subclass", choices=[]
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