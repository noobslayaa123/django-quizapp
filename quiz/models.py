# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Player(models.Model):
    pid = models.AutoField(primary_key=True)
    playername = models.CharField(unique=True, max_length=100)
    live_sts = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class PlayerQuestions(models.Model):
    srno = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Player, models.DO_NOTHING, db_column='pid')
    questionid = models.ForeignKey('TbQuestions', models.DO_NOTHING, db_column='questionid')
    choice = models.IntegerField()
    

    class Meta:
        managed = False
        db_table = 'player_questions'


class PlayerQuizdet(models.Model):
    srno = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Player, models.DO_NOTHING, db_column='pid')
    quizid = models.ForeignKey('TblQuizlist', models.DO_NOTHING, db_column='quizid')
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_quizdet'


class QuizImgupload(models.Model):
    image = models.CharField(max_length=100)
    quiz = models.ForeignKey('TblQuizlist', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quiz_imgupload'


class TbQuestions(models.Model):
    questionid = models.AutoField(primary_key=True)
    question = models.CharField(unique=True, max_length=255)
    quizid = models.ForeignKey('TblQuizlist', models.DO_NOTHING, db_column='quizid')

    def __str__(self):
        return self.question

    class Meta:
        managed = False
        db_table = 'tb_questions'


class TblChoices(models.Model):
    questionid = models.OneToOneField(TbQuestions, models.DO_NOTHING, db_column='questionid', primary_key=True)
    choice1 = models.CharField(max_length=100, blank=True, null=True)
    choice2 = models.CharField(max_length=100, blank=True, null=True)
    choice3 = models.CharField(max_length=100)


    def __str__(self):
        return self.choice3

    class Meta:
        managed = False
        db_table = 'tbl_choices'


class TblQuizlist(models.Model):
    quizid = models.IntegerField(primary_key=True)
    quizstatus = models.IntegerField(blank=True, null=True)
    quizdate = models.DateTimeField(blank=True, null=True)
    quizname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.quizname

    class Meta:
        managed = False
        db_table = 'tbl_quizlist'
