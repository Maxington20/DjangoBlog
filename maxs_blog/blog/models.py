from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(unique=True, populate_from='title')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pub_date']
    
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.URLField(default='https://google.com')
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Image for {self.post.title}"