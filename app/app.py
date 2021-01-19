from flask import Flask, redirect,request,url_for
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_security import SQLAlchemyUserDatastore,Security,current_user




app = Flask(__name__, static_folder='templates/static')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

## Миграции ##
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

## ADMIN ##
from models import *

class AdminMixin:
    def is_accessible(self):
        """
        проверяет доступность действия для пользователя
        """
        return current_user.has_role('admin')

    def inaccessible_callback(self,name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form,model,is_created)

class AdminView(AdminMixin,ModelView):
    """
    переопределяем методы is_accessible, inaccessible_callback из ModelVIew
    """
    pass

class HomeAdminView(AdminMixin,AdminIndexView):
    pass

admin = Admin(app,'FlaskApp',url='/admin',template_mode='bootstrap4',index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(Post, db.session))

## Flask Security ##
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
