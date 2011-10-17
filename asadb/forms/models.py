from django.db import models

import datetime
import os, errno

import settings
import groups.models
from util.misc import log_and_ignore_failures, mkdir_p
import util.previews

class FYSM(models.Model):
    group = models.ForeignKey(groups.models.Group)
    display_name = models.CharField(max_length=50)
    year = models.IntegerField()
    website = models.URLField()
    join_url = models.URLField(verbose_name="recruiting URL", help_text="""<p>If you have a specific web page for recruiting new members of your group, you can link to it here. It will be used as the destination for most links about your group (join link on the main listing page and when clicking on the slide, but not the "website" link on the slide page). If you do not have such a page, use your main website's URL.</p>""")
    contact_email = models.EmailField(help_text="Give an address for students interested in joining the group to email (e.g., an officers list)")
    description = models.TextField(help_text="Explain in about three or four sentences what your group does and why incoming freshmen should get involved. If you go over 400 characters, we may ask you to cut your description, cut it ourselves, and/or display only the beginning on the group listing pages.")
    logo = models.ImageField(upload_to='fysm/logos', blank=True, )
    slide = models.ImageField(upload_to='fysm/slides', default="", help_text="Upload a slide to display on the group detail page. This will be scaled to be at most 600x600 pixels. We recommend making it exactly that size.")
    tags = models.CharField(max_length=100, blank=True, help_text="Specify some free-form, comma-delimited tags for your group", )
    categories = models.ManyToManyField('FYSMCategory', blank=True, help_text="Put your group into whichever of our categories seem applicable.", )
    join_preview = models.ForeignKey('PagePreview', null=True, )

    def save(self, *args, **kwargs):
        if self.join_preview is None or self.join_url != self.join_preview.url:
            self.join_preview = PagePreview.allocate_page_preview(
                filename='fysm/%d/group%d'%(self.year, self.group.pk, ),
                url=self.join_url,
            )
        super(FYSM, self).save(*args, **kwargs) # Call the "real" save() method.

    def __str__(self, ):
        return "%s (%d)" % (self.display_name, self.year, )

    class Meta:
        verbose_name = "FYSM submission"

class FYSMCategory(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()
    blurb = models.TextField()

    def __str__(self, ):
        return self.name

    class Meta:
        verbose_name = "FYSM category"
        verbose_name_plural = "FYSM categories"
        ordering = ['name', ]

class FYSMView(models.Model):
    when = models.DateTimeField(default=datetime.datetime.now)
    fysm = models.ForeignKey(FYSM, null=True, blank=True, )
    year = models.IntegerField(null=True, blank=True, )
    page = models.CharField(max_length=20, blank=True, )
    referer = models.URLField(verify_exists=False, null=True, )
    user_agent = models.CharField(max_length=255)
    source_ip = models.IPAddressField()
    source_user = models.CharField(max_length=30, blank=True, )

    @staticmethod
    @log_and_ignore_failures(logfile=settings.LOGFILE)
    def record_metric(request, fysm=None, year=None, page=None, ):
        record = FYSMView()
        record.fysm = fysm
        record.year = year
        record.page = page
        if 'HTTP_REFERER' in request.META:
            record.referer = request.META['HTTP_REFERER']
        record.user_agent = request.META['HTTP_USER_AGENT']
        record.source_ip = request.META['REMOTE_ADDR']
        record.source_user = request.user.username
        record.save()

class PagePreview(models.Model):
    update_time = models.DateTimeField(default=datetime.datetime.utcfromtimestamp(0))
    url = models.URLField()
    image = models.ImageField(upload_to='page-previews', blank=True, )

    never_updated = datetime.datetime.utcfromtimestamp(0) # Never updated
    update_interval = datetime.timedelta(hours=23)

    def image_filename(self, ):
        return os.path.join(settings.MEDIA_ROOT, self.image.name)


    @classmethod
    def allocate_page_preview(cls, filename, url, ):
        preview = PagePreview()
        preview.update_time = cls.never_updated
        preview.url = url
        preview.image = 'page-previews/%s.jpg' % (filename, )
        image_filename = preview.image_filename()
        mkdir_p(os.path.dirname(image_filename))
        try:
            os.symlink('no-preview.jpg', image_filename)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise
        preview.save()
        return preview

    def update_preview(self, ):
        self.update_time = datetime.datetime.now()
        self.save()
        failure = util.previews.generate_webpage_preview(self.url, self.image_filename(), )
        if failure:
            self.update_time = self.never_updated
            self.save()

    @classmethod
    def previews_needing_updates(cls, interval=None, ):
        if interval is None:
            interval = cls.update_interval
        before = datetime.datetime.now() - interval
        return cls.objects.filter(update_time__lte=before)

    @classmethod
    def update_outdated_previews(cls, interval=None, ):
        previews = cls.previews_needing_updates(interval)
        now = datetime.datetime.now()
        update_list = []
        previews_dict = {}
        for preview in previews:
            update_list.append((preview.url, preview.image_filename(), ))
            previews_dict[preview.url] = preview
            preview.update_time = now
            preview.save()
        failures = util.previews.generate_webpage_previews(update_list)
        for url, msg in failures:
            print "%s: %s" % (url, msg, )
            preview = previews_dict[url]
            preview.update_time = cls.never_updated
            preview.save()


class GroupConfirmationCycle(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    create_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self, ):
        return u"GroupConfirmationCycle %d: %s" % (self.id, self.name, )

    @classmethod
    def latest(cls, ):
        return cls.objects.order_by('-create_date')[0]


class GroupMembershipUpdate(models.Model):
    update_time = models.DateTimeField(default=datetime.datetime.utcfromtimestamp(0))
    updater_name = models.CharField(max_length=30)
    updater_title = models.CharField(max_length=30, help_text="You need not hold any particular title in the group, but we like to know who is completing the form.")
    
    group = models.ForeignKey(groups.models.Group, help_text="If your group does not appear in the list above, then please email asa-exec@mit.edu.")
    group_email = models.EmailField(help_text="The text of the law will be automatically distributed to your members via this list, in order to comply with the law.")
    officer_email = models.EmailField()

    membership_definition = models.TextField()
    num_undergrads = models.IntegerField()
    num_grads = models.IntegerField()
    num_alum = models.IntegerField()
    num_other_affiliate = models.IntegerField()
    num_other = models.IntegerField()

    membership_list = models.TextField(help_text="Member emails on separate lines (Athena usernames where applicable)")

    email_preface = models.TextField(blank=True, help_text="If you would like, you may add text here that will preface the text of the policies when it is sent out to the group membership list provided above.")

    hazing_statement = "By checking this, I hereby affirm that I have read and understand Chapter 269: Sections 17, 18, and 19 of Massachusetts Law. I furthermore attest that I have provided the appropriate address or will otherwise distribute to group members, pledges, and/or applicants, copies of Massachusetts Law 269: 17, 18, 19 and that our organization, group, or team agrees to comply with the provisions of that law. (See below for text.)"
    no_hazing = models.BooleanField(help_text=hazing_statement)

    discrimination_statement = "By checking this, I hereby affirm that I have read and understand the MIT Non-Discrimination Policy.  I furthermore attest that our organization, group, or team agrees to not discriminate against individuals on the basis of race, color, sex, sexual orientation, gender identity, religion, disability, age, genetic information, veteran status, ancestry, or national or ethnic origin."
    no_discrimination = models.BooleanField(help_text=discrimination_statement)

    def __unicode__(self, ):
        return "GroupMembershipUpdate for %s" % (self.group, )


VALID_UNSET         = 0
VALID_AUTOVALIDATED = 10
VALID_OVERRIDDEN    = 20    # confirmed by an admin
VALID_AUTOREJECTED      = -10
VALID_HANDREJECTED      = -20
VALID_CHOICES = (
    (VALID_UNSET,           "unvalidated"),
    (VALID_AUTOVALIDATED,   "autovalidated"),
    (VALID_OVERRIDDEN,      "hand-validated"),
    (VALID_AUTOREJECTED,    "autorejected"),
    (VALID_HANDREJECTED,    "hand-rejected"),
)

class PersonMembershipUpdate(models.Model):
    update_time = models.DateTimeField(default=datetime.datetime.utcfromtimestamp(0))
    username = models.CharField(max_length=30)
    cycle = models.ForeignKey(GroupConfirmationCycle)
    deleted = models.DateTimeField(default=None, null=True, blank=True, )
    valid = models.IntegerField(choices=VALID_CHOICES, default=VALID_UNSET)
    groups = models.ManyToManyField(groups.models.Group, help_text="By selecting a group here, you indicate that you are an active member of the group in question.<br>If your group does not appear in the list above, then please email asa-exec@mit.edu.<br>")

    def __unicode__(self, ):
        return "PersonMembershipUpdate for %s" % (self.username, )
