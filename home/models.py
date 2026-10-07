from django.db import models


class HomePage(models.Model):
    title = models.CharField(max_length=200, default='Welcome Home')
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='home/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    title = models.CharField(max_length=200, default='About Us')
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'

    def __str__(self):
        return self.title


class BranchPage(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    pastor_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class EventPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']
        verbose_name = 'Event Page'
        verbose_name_plural = 'Event Pages'

    def __str__(self):
        return self.title


class MagazinePage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    month = models.CharField(max_length=20, blank=True)
    year = models.PositiveIntegerField(default=2026)
    cover_image = models.ImageField(upload_to='magazine/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='magazine/pdf/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-published_at']
        verbose_name = 'Magazine Page'
        verbose_name_plural = 'Magazine Pages'

    def __str__(self):
        return self.title


class MusicPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    audio_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='music/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Music Page'
        verbose_name_plural = 'Music Pages'

    def __str__(self):
        return self.title


class MediaPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=50, default='video')
    external_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Media Page'
        verbose_name_plural = 'Media Pages'

    def __str__(self):
        return self.title


class CommunityPage(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    category = models.CharField(max_length=50, default='announcement')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Community Page'
        verbose_name_plural = 'Community Pages'

    def __str__(self):
        return self.title


class ContactPage(models.Model):
    title = models.CharField(max_length=200, default='Contact Us')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Pages'

    def __str__(self):
        return self.title


class SectionContent(models.Model):
    MAIN_HEADING_CHOICES = (
        ('About', 'About'),
        ('Branches', 'Branches'),
        ('Events', 'Events'),
        ('Community', 'Community'),
        ('Music', 'Music'),
        ('Media', 'Media'),
        ('Magazine', 'Magazine'),
        ('Contact', 'Contact'),
    )

    SUBHEADING_GROUPS = (
        ('About', ('About Church', 'Church History', 'Branches')),
        ('Branches', (
            'CSI Christ Church, Kambenery',
            'CSI Christ Church, Sundarapandiyapuram',
            'CSI Rhenius Memorial Church, Bharathi Nagar',
            'CSI Christ Church, Poigai-Kovilaandanoor',
        )),
        ('Events', (
            'Upcoming Events',
            'Church Activities',
            'Important Events',
            'Special Festivals',
            'Prayer Meetings',
            'Camps',
            'Retreats',
            'Missionaries Place Travel',
        )),
        ('Community', ('Sunday School', 'Youth Fellowship', "Women's Fellowship", "Men's Fellowship")),
        ('Music', ('Keerthanai Songs', 'K.V. Songs', 'New Songs', 'Music Training')),
        ('Media', ('Short Videos', 'Long Videos', 'Live')),
        ('Magazine', ('Magazine Issue', 'Magazine Article', 'Bible Verse', 'Magazine Photo')),
        ('Contact', ('Contact', 'Prayer Requests', 'Visit the Church')),
    )

    SUBHEADING_CHOICES = tuple(
        (subheading, subheading)
        for _, subheadings in SUBHEADING_GROUPS
        for subheading in subheadings
    )

    main_heading = models.CharField(max_length=50, choices=MAIN_HEADING_CHOICES)
    subheading = models.CharField(max_length=200, choices=SUBHEADING_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='section-content/', blank=True, null=True)
    media_url = models.URLField(blank=True)
    event_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subheading Content'
        verbose_name_plural = 'Subheading Content'

    def __str__(self):
        return self.title or self.subheading
