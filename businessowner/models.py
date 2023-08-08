from django.db import models
from djongo import models
from django.core.validators import FileExtensionValidator, RegexValidator
from django.conf import settings
from django.utils.timezone import now
import uuid
from superadmin.models import *

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class CompetitiveBatches(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_name = models.CharField(max_length=50, unique=True)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False )
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(CompetitiveBatches, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.batch_name
class CompetitiveSubjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=50, unique=True)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_subject")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(CompetitiveSubjects, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.subject_name
class CompetitiveChapters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.ForeignKey(CompetitiveSubjects, on_delete=models.CASCADE, related_name="competitive_subject")
    chapter_name = models.CharField(max_length=50, unique=True)
    batches = models.ArrayReferenceField(CompetitiveBatches)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(CompetitiveBatches, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.chapter_name
class Options(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    option1 = models.CharField(("a"), max_length=50) 
    option2 = models.CharField(("b"), max_length=50)
    option3 = models.CharField(("c"), max_length=50)
    option4 = models.CharField(("d"), max_length=50)
    # option5 = models.CharField(("e"), null=True, default=False)
    objects = models.DjongoManager()



class CompetitiveQuestions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competitve_chapter = models.ForeignKey(CompetitiveChapters, on_delete=models.CASCADE, related_name="question_chapter")
    question = models.CharField(max_length=100)
    options = models.ArrayField(Options)
    answer = models.CharField(max_length=100)
    QUESTION_CHOICES = (('easy','easy'),('medium','medium'), ('hard', 'hard'))
    question_category = models.CharField(("Question Category"),choices=QUESTION_CHOICES, max_length=50,default='easy')
    marks = models.IntegerField()
    time_duration = models.TimeField()
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="competitive_question")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("Status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(CompetitiveQuestions, self).delete()
        else:
            self.deleted_at = now()
            self.save()



class CompetitiveExamData(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    subject = models.ForeignKey(CompetitiveSubjects, on_delete=models.CASCADE, related_name="examdata_comp_subject")
    chapter = models.ArrayReferenceField(CompetitiveChapters)
    easy_question = models.IntegerField()
    medium_question = models.IntegerField()
    hard_question = models.IntegerField()
    time_per_subject = models.DateTimeField()
    marks_per_subject = models.IntegerField()
    objects = models.DjongoManager()

    

class CompetitiveExams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="competitive_exam")
    exam_title = models.CharField(max_length=50)
    batch = models.ForeignKey(CompetitiveBatches, on_delete=models.CASCADE, related_name="exam_batch")
    total_questions = models.IntegerField()
    time_duration = models.IntegerField()
    passing_marks = models.IntegerField()
    total_marks = models.IntegerField()
    MARKS_CHOICES = (('None','None'),('0.25','0.25'), ('0.33', '0.33'))
    negative_marks = models.CharField(("negative_marks"),choices=MARKS_CHOICES, max_length=50,default='None')
    exam_data = models.ArrayReferenceField(CompetitiveExamData)
    option_e = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(CompetitiveExams, self).delete()
        else:
            self.deleted_at = now()
            self.save()
    def __str__(self):
        return self.exam_title

class AcademicBoards(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board_name = models.CharField(max_length=50, unique=True)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_academic")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicBoards, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.board_name

class AcademicMediums(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medium_name = models.CharField(max_length=50, unique=True)
    board_name = models.ForeignKey(AcademicBoards, on_delete=models.CASCADE, related_name="academic_boards")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicMediums, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.medium_name
class AcademicStandards(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    standard = models.CharField(max_length=50, unique=True)
    medium_name = models.ForeignKey(AcademicMediums, on_delete=models.CASCADE, related_name="academic_mediums")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicStandards, self).delete()
        else:
            self.deleted_at = now()
            self.save()
    def __str__(self):
        return self.standard
class AcademicSubjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=50, unique=True)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="academic_standards")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicStandards, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.subject_name
class AcademicChapters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter_name = models.CharField(max_length=50, unique=True)
    subject_name = models.ForeignKey(AcademicSubjects, on_delete=models.CASCADE, related_name="academic_subjects")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicStandards, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.chapter_name
class Students(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_student")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_number = models.IntegerField()
    parent_name = models.CharField(max_length=50)
    parent_contact_no = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{10}$")], max_length=10)
    profile_image = models.ImageField(blank=True, upload_to="students", validators=[FileExtensionValidator(['jpg','jpeg','png'])], max_length=None, null=True)
    address = models.TextField()
    batch = models.ForeignKey(CompetitiveBatches, on_delete=models.CASCADE, related_name="student_batch", null=True)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="student_standard", null=True)
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Students, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.email

class AcademicQuestions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_chapter = models.ForeignKey(AcademicChapters, on_delete=models.CASCADE, related_name="academic_chapter")
    question = models.CharField(max_length=100)
    options = models.ArrayField(Options,max_length=100)
    answer = models.CharField(max_length=100)
    QUESTION_CHOICES = (('easy','easy'),('medium','medium'), ('hard', 'hard'))
    question_category = models.CharField(("question_category"),choices=QUESTION_CHOICES, max_length=50,default='easy')
    marks = models.IntegerField()
    time_duration = models.TimeField()
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="academic_question")
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicQuestions, self).delete()
        else:
            self.deleted_at = now()
            self.save()





class AcademicExamData(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    subject = models.ForeignKey(AcademicSubjects, on_delete=models.CASCADE)
    chapter = models.ArrayReferenceField(AcademicChapters)
    easy_question = models.IntegerField()
    medium_question = models.IntegerField()
    hard_question = models.IntegerField()
    time_per_subject = models.DateTimeField()
    marks_per_subject = models.IntegerField()
    objects = models.DjongoManager()

    


class AcademicExams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="academic_exam")
    exam_title = models.CharField(max_length=50)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="exam_standard")
    total_questions = models.IntegerField()
    time_duration = models.IntegerField()
    passing_marks = models.IntegerField()
    total_marks = models.IntegerField()
    MARKS_CHOICES = (('None','None'),('0.25','0.25'), ('0.33', '0.33'))
    negative_marks = models.CharField(("negative_marks"),choices=MARKS_CHOICES, max_length=50,default='None')
    exam_data = models.ArrayReferenceField(AcademicExamData)
    option_e = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    CHOICES = (('inactive','inactive'),('active','active'))
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicExams, self).delete()
        else:
            self.deleted_at = now()
            self.save()
    def __str__(self):
        return self.exam_title

class Results(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competitive_exam = models.ForeignKey(CompetitiveExams, on_delete=models.CASCADE, related_name="competitive_result")
    academic_exam = models.ForeignKey(AcademicBoards, on_delete=models.CASCADE, related_name="academic_result") 
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_result")
    score = models.FloatField()
    CHOICES = (('pass','pass'),('fail','fail'))
    result = models.CharField(("result"),choices=CHOICES, max_length=50,default='pass')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(AcademicExams, self).delete()
        else:
            self.deleted_at = now()
            self.save()