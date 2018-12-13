from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db
from main.libs import bcrypt_custom
from main.models.assoc_tables import user_role, user_permission, user_control


class UserModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'user'

    username = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    bio = db.Column(db.Text)
    password = db.Column(db.String(256))
    password_salt = db.Column(db.String(64))
    google_id = db.Column(db.String(32), unique=True)
    image_url = db.Column(db.String(512))
    token = db.Column(db.String(512))

    # Many to many
    permissions = relationship('PermissionModel', secondary=user_permission)
    controls = relationship('ControlModel', secondary=user_control)
    roles = relationship('RoleModel', secondary=user_role)

    # One to many
    articles = relationship('ArticleModel', back_populates='user')
    comments = relationship('CommentModel', back_populates='user')
    logs = relationship('LogModel', backref=db.backref('user'))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

        if kwargs.get('password'):
            self.set_password(kwargs.get('password'))

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password, self.password_salt = \
            bcrypt_custom.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt_custom.check_password_hash(
            self.password, self.password_salt, value
        )

    def get_id(self):
        return self.id
