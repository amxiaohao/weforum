from __future__ import unicode_literals

from datetime import datetime

import markdown

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=128, null=True, blank=True)
    content = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=PUBLISHED)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name='+')
    update_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-create_date', )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Article, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        super(Article, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_published():
        articles = Article.objects.filter(status=Article.PUBLISHED)
        return articles

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(), 
                                                       article=self)

    def get_tags(self):
        return Tag.objects.filter(article=self)

    def get_summary(self):
        if len(self.content) > 100:
            return "{0}...".format(self.content[:100])
        else:
            return self.content

    def get_summary_as_markdowm(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return ArticleComment.objects.filter(article=self)


class Tag(models.Model):
    article = models.ForeignKey(Article)
    tag = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        unique_together = (('tag', 'article'), )
        index_together = [['tag', 'article'], ]

    def __unicode__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for t in tags:
            if t.article.status == Article.PUBLISHED:
                if t.tag in count:
                    count[t.tag] = count[t.tag] + 1
                else:
                    count[t.tag] = 1
        sorted_tags = sorted(count.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags[:10]


class ArticleComment(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'
        ordering = ('-date', )

    def __unicode__(self):
        return "{0} - {1}".format(self.user.username, self.article.title)