# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Worklist(models.Model):
    no = models.CharField(max_length=10)
    유형 = models.CharField(max_length=20)
    명칭 = models.CharField(max_length=250)
    nid = models.CharField(max_length=10)
    lcode = models.CharField(max_length=10)
    준공일 = models.DateField()
    구축시한 = models.DateField()
    실사구분 = models.CharField(max_length=10)
    실사일정 = models.DateField(blank=True, null=True)
    poi구분 = models.CharField(max_length=10)
    poi구축일 = models.CharField(max_length=10, blank=True, null=True)
    net구분 = models.CharField(max_length=10)
    net구축일 = models.CharField(max_length=10, blank=True, null=True)
    map구분 = models.CharField(max_length=10)
    map구축일 = models.CharField(max_length=10, blank=True, null=True)
    데이터확인 = models.CharField(max_length=5)
    서비스확인 = models.CharField(max_length=5)
    자료정보 = models.CharField(max_length=250, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    작성자 = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'worklist'

    def __str__(self):
        return self.no