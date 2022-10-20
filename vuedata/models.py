from django.db import models

# Create your models here.

class userTable(models.Model):
    UserName = models.CharField(max_length=32)
    Password = models.BinaryField(max_length=64)
    Email = models.CharField(max_length=32)
    Sex = models.CharField(max_length=1)
    Birthday = models.DateField()
    Phone = models.CharField(max_length=32)
    Salt = models.BinaryField(max_length=32)

class applyTable(models.Model):
    RegistrationNumber = models.CharField(max_length=32)
    SerialNumber = models.CharField(max_length=32)
    Organization = models.CharField(max_length=32)
    StartTime = models.DateField()
    EndTime = models.DateField()
    JuridicalPerson= models.CharField(max_length=32)
    ChargePerson= models.CharField(max_length=32)
    ChargePhone= models.CharField(max_length=32)
    UserName= models.CharField(max_length=32)
    PublicKey=models.CharField(max_length=32)

class certTable(models.Model):
    RegistrationNumber = models.CharField(max_length=32)
    SerialNumber = models.CharField(max_length=32)
    Organization = models.CharField(max_length=32)
    StartTime = models.DateField()
    EndTime = models.DateField()
    JuridicalPerson= models.CharField(max_length=32)
    ChargePerson= models.CharField(max_length=32)
    ChargePhone= models.CharField(max_length=32)
    UserName= models.CharField(max_length=32)
    PublicKey=models.CharField(max_length=32)
    CertPathName=models.CharField(max_length=32)

class crlTable(models.Model):
    SerialNumber=models.CharField(max_length=32)
    Organization=models.CharField(max_length=32)
    RevokeTime = models.DateField()



