from django.db import models
from djongo import models
from django.core.validators import FileExtensionValidator, RegexValidator
from django.conf import settings
from django.utils.timezone import now
import uuid
from django.utils.html import mark_safe


class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)
    

#------------------------------------------------------------------------------------------------#
#----------------------------------------SUPERADMIN----------------------------------------------#
#------------------------------------------------------------------------------------------------#


class States(models.Model):
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("State*"), max_length=50,unique=True)
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   

    def delete(self, hard=False, **kwargs):
        if hard:
            super(States, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1. States"


class Cities(models.Model):
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.ForeignKey(States, on_delete=models.CASCADE, related_name="state", verbose_name="State*")
    name = models.CharField(("City*"), max_length=50,unique=True)
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Cities, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "2. Cities"


class BusinessOwners(models.Model):
    BUSINESS_CHOICES = (('competitive','competitive'),('academic','academic'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(max_length=50,verbose_name='Business Name*')
    business_type = models.CharField(("Business Type*"),choices=BUSINESS_CHOICES, max_length=50)
    first_name = models.CharField(max_length=50,verbose_name='First Name*')
    last_name = models.CharField(max_length=50,verbose_name='Last Name*')
    email = models.EmailField(unique=True, verbose_name='Email*')
    password = models.CharField(max_length=40, verbose_name='Password*')
    contact_no = models.CharField(validators=[RegexValidator(regex=r"^(?:\+?1)?\d{10}$")], max_length=10, unique=True, verbose_name='Contact No*')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name="owner_city", verbose_name='City*')
    address = models.TextField(verbose_name='Address*')
    logo = models.ImageField(blank=True, upload_to="owner", validators=[FileExtensionValidator(['jpg','jpeg','png'])], height_field=None, width_field=None, max_length=None, null=True)
    tuition_tagline = models.CharField(max_length=50, null=True, verbose_name='Tuition Tagline', blank=True) 
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()   

    def delete(self, hard=False, **kwargs):
        if hard:
            super(BusinessOwners, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.business_name
    
    class Meta:
        verbose_name_plural = "3. Business Owners"

    def image_tag(self):
            return mark_safe('<img src="/directory/%s" width="150" height="150" />' % (self.logo))


class Plans(models.Model):
    PLAN_CHOICES = ((3, '3 months'), (6, '6 months'), (9, '9 months'), (12, '12 months'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_name = models.CharField(max_length=50, verbose_name='Plan Name*')
    description = models.TextField(verbose_name='Description*')
    price = models.FloatField(verbose_name='Price*')
    validity = models.IntegerField(choices=PLAN_CHOICES,default='3', verbose_name='Validity*')
    image = models.ImageField(blank=True, upload_to="plan", validators=[FileExtensionValidator(['jpg','jpeg','png'])], height_field=None, width_field=None, max_length=None)
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Plans, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.plan_name
    
    class Meta:
        verbose_name_plural = "4. Plans"


class PurchaseHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE, related_name="plan")
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner")
    order_id = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Plans, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return f"{self.plan.plan_name} ({self.business_owner.first_name} {self.business_owner.last_name})"
    

class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ArrayReferenceField(BusinessOwners, verbose_name='Business Owner')
    title = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None, editable=False)
    objects = ParanoidModelManager()
    
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Notifications, self).delete()
        else:
            self.deleted_at = now()
            self.save()
            
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "5. Notifications"


#------------------------------------------------------------------------------------------------#
#---------------------------------------BUSINESS-OWNER-------------------------------------------#
#------------------------------------------------------------------------------------------------#        

class CompetitiveBatches(models.Model):
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_name = models.CharField(max_length=50, unique=True)
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=50, unique=True)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_subject")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.ForeignKey(CompetitiveSubjects, on_delete=models.CASCADE, related_name="competitive_subject")
    chapter_name = models.CharField(max_length=50, unique=True)
    batches = models.ArrayReferenceField(CompetitiveBatches)
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
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False)
    option1 = models.CharField(("a"), max_length=50) 
    option2 = models.CharField(("b"), max_length=50)
    option3 = models.CharField(("c"), max_length=50, blank=True, null=True)
    option4 = models.CharField(("d"), max_length=50, blank=True, null=True)
    # option5 = models.CharField(("e"), null=True, default=False, )
    objects = models.DjongoManager()
   

class CompetitiveQuestions(models.Model):
    QUESTION_CHOICES = (('easy','easy'),('medium','medium'), ('hard', 'hard'))
    ANSWER_CHOICES = (('option1','option1'),('option2','option2'), ('option3', 'option3'), ('option4', 'option4'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competitve_chapter = models.ForeignKey(CompetitiveChapters, on_delete=models.CASCADE, related_name="question_chapter")
    question = models.CharField(max_length=100)
    options = models.ForeignKey(Options, on_delete=models.CASCADE)
    answer = models.CharField(("Right Answer"),choices=ANSWER_CHOICES, max_length=50)
    question_category = models.CharField(("Question Category"),choices=QUESTION_CHOICES, max_length=50,default='easy')
    marks = models.IntegerField()
    time_duration = models.TimeField()
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="competitive_question")
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
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False)
    subject = models.ForeignKey(CompetitiveSubjects, on_delete=models.CASCADE, related_name="examdata_comp_subject")
    chapter = models.ArrayReferenceField(CompetitiveChapters)
    easy_question = models.IntegerField()
    medium_question = models.IntegerField()
    hard_question = models.IntegerField()
    time_per_subject = models.DateTimeField()
    marks_per_subject = models.IntegerField()
    objects = models.DjongoManager()

    
class CompetitiveExams(models.Model):
    MARKS_CHOICES = (('None','None'),('0.25','0.25'), ('0.33', '0.33'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="competitive_exam")
    exam_title = models.CharField(max_length=50)
    batch = models.ForeignKey(CompetitiveBatches, on_delete=models.CASCADE, related_name="exam_batch")
    total_questions = models.IntegerField()
    time_duration = models.IntegerField()
    passing_marks = models.IntegerField()
    total_marks = models.IntegerField()
    negative_marks = models.CharField(("negative_marks"),choices=MARKS_CHOICES, max_length=50,default='None')
    exam_data = models.ArrayReferenceField(CompetitiveExamData)
    option_e = models.BooleanField(default=False)
    start_date = models.DateTimeField()
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
    
    class Meta:
        verbose_name_plural = "6. Competitive Exams"


class AcademicBoards(models.Model):
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board_name = models.CharField(max_length=50, unique=True)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_academic")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medium_name = models.CharField(max_length=50, unique=True)
    board_name = models.ForeignKey(AcademicBoards, on_delete=models.CASCADE, related_name="academic_boards")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    standard = models.CharField(max_length=50, unique=True)
    medium_name = models.ForeignKey(AcademicMediums, on_delete=models.CASCADE, related_name="academic_mediums")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=50, unique=True)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="academic_standards")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter_name = models.CharField(max_length=50, unique=True)
    subject_name = models.ForeignKey(AcademicSubjects, on_delete=models.CASCADE, related_name="academic_subjects")
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
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="owner_student")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{10}$")], max_length=10)
    parent_name = models.CharField(max_length=50)
    parent_contact_no = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{10}$")], max_length=10)
    profile_image = models.ImageField(blank=True, upload_to="students", validators=[FileExtensionValidator(['jpg','jpeg','png'])], max_length=None, null=True)
    address = models.TextField()
    batch = models.ForeignKey(CompetitiveBatches, on_delete=models.CASCADE, related_name="student_batch", null=True, blank=True)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="student_standard", null=True, blank=True)
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
    
    class Meta:
        verbose_name_plural = "8. Students"

class AcademicQuestions(models.Model):
    QUESTION_CHOICES = (('easy','easy'),('medium','medium'), ('hard', 'hard'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_chapter = models.ForeignKey(AcademicChapters, on_delete=models.CASCADE, related_name="academic_chapter")
    question = models.CharField(max_length=100) 
    options = models.ForeignKey(Options, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    question_category = models.CharField(("question_category"),choices=QUESTION_CHOICES, max_length=50,default='easy')
    marks = models.IntegerField()
    time_duration = models.TimeField()
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="academic_question")
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
            
    def __str__(self):
        return self.question

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
    MARKS_CHOICES = (('None','None'),('0.25','0.25'), ('0.33', '0.33'))
    CHOICES = (('inactive','inactive'),('active','active'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_owner = models.ForeignKey(BusinessOwners, on_delete=models.CASCADE, related_name="academic_exam")
    exam_title = models.CharField(max_length=50)
    standard = models.ForeignKey(AcademicStandards, on_delete=models.CASCADE, related_name="exam_standard")
    total_questions = models.IntegerField()
    time_duration = models.IntegerField()
    passing_marks = models.IntegerField()
    total_marks = models.IntegerField()
    negative_marks = models.CharField(("negative_marks"),choices=MARKS_CHOICES, max_length=50,default='None')
    exam_data = models.ArrayReferenceField(AcademicExamData)
    option_e = models.BooleanField(default=False)
    start_date = models.DateTimeField()
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
    
    class Meta:
        verbose_name_plural = "7. Academic Exams"


class Results(models.Model):
    CHOICES = (('pass','pass'),('fail','fail'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competitive_exam = models.ForeignKey(CompetitiveExams, on_delete=models.CASCADE, related_name="competitive_result")
    academic_exam = models.ForeignKey(AcademicBoards, on_delete=models.CASCADE, related_name="academic_result") 
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_result")
    score = models.FloatField() 
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