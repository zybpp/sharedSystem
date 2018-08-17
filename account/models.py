from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .managers import UserInheritanceManager, UserManager
from datetime import date

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    USERS_AUTO_ACTIVATE = not settings.USERS_VERIFY_EMAIL

    email = models.EmailField(
        _('email address'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=USERS_AUTO_ACTIVATE,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    user_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, editable=False)

    objects = UserInheritanceManager()
    base_objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])

    def activate(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.user_type_id:
            self.user_type = ContentType.objects.get_for_model(self, for_concrete_model=False)
        super(AbstractUser, self).save(*args, **kwargs)


class User(AbstractUser):

    """
    Concrete class of AbstractUser.
    Use this if you don't need to extend User.
    """
    user = models.CharField(max_length=30, default="admin", verbose_name="用户名", unique=True)
    name = models.CharField(max_length=30, default="admin", verbose_name="姓名")
    sex = models.CharField(max_length=10, default="帅哥/美女", verbose_name="性别")
    birthday = models.CharField(max_length=30, default="1991-08-07", verbose_name="生日")
    email = models.EmailField( _('邮箱'), max_length=255, unique=True, db_index=True)
    password = models.CharField(_('密码'), max_length=128)
    job_number = models.CharField(max_length=30, default="W010000001", verbose_name="工号")
    position = models.CharField(max_length=50, default="Android 软件开发工程师", verbose_name="职位")
    department = models.CharField(max_length=50, default="Android 系统开发部", verbose_name="部门")
    phone_number = models.CharField(max_length=30, default="12345678912", verbose_name="电话号码")

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.name

    def age(self):
        current_date = date.today()
        b_year = self.birthday[:4]
        b_month = self.birthday[5:7]
        b_day = self.birthday[8:]

        age = int(current_date.year) - int(b_year) - 1
        if int(current_date.month) > int(b_month):
            age += 1
        elif int(current_date.month) == int(b_month):
            if int(current_date.day) > int(b_day):
                age += 1
        return age


