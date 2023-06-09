
"""Blog listing and blog detail pages."""
from django import forms
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.template.defaultfilters import slugify

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import Tag, TaggedItemBase

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from .utils import unique_slugify

from page.blocks import BaseStreamBlock


@register_snippet
class Author(ClusterableModel):
    """
    A Django model to store Author objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)

    `Author` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    email = models.EmailField(blank=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+",
    )

    panels = [
        FieldPanel("image"),
        MultiFieldPanel(
            [
                FieldPanel("first_name", classname="col6"),
                FieldPanel("last_name", classname="col6"),
            ],
            "Name",
        ),
        FieldPanel("slug"),
        FieldPanel("email"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ""

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    # save model and create unique slug url
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(f"{ self.first_name }-{ self.last_name }")
            unique_slugify(self, slug)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class ArticlePeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.

    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """

    page = ParentalKey(
        "ArticlePage", related_name="article_person_relationship", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        "Author", related_name="person_article_relationship", on_delete=models.CASCADE
    )
    panels = [FieldPanel("author")]


@register_snippet
class ArticleCategory(models.Model):
    """Article catgory for a snippet."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        unique=True,
        null=True,
        blank=True,
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify articles by this category.\
        This is auto-generated on save',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    # save model and create unique slug url
    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class ArticlePageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the Article Detail Page object and tags. There's a longer guide on using it at
    http://docs.wagtail.io/en/latest/reference/pages/model_recipes.html#tagging
    """

    content_object = ParentalKey(
        "ArticlePage", related_name="tagged_items", on_delete=models.CASCADE
    )


class ArticleIndexPage(RoutablePageMixin, Page):
    """Index page lists all the Article  Pages."""
    pass

    # Speficies that only ArticlePage objects can live under this index page
    subpage_types = ["ArticlePage"]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["articles"] = ArticlePage.objects.live().public()
        context["categories"] = ArticleCategory.objects.all()
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related BlogPages for a given Tag or redirect back to the BlogIndexPage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    @route(r"^tags/$")
    def all_article_tags(self, request):
        tags = ArticlePageTag.objects.all().order_by("tag__name")
        context = {"tags": tags}
        return render(request, "article/article_tags_index_page.html", context)

    # Returns the child Article  Page objects for this Article Index Page.
    # If a tag is used then it will filter the articles by tag.
    def get_articles(self, tag=None):
        articles = ArticlePage.objects.live().descendant_of(self)
        if tag:
            articles = articles.filter(tags=tag)
        return articles

    @route(r"^tags/([\w-]+)/$")
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no articles tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        articles = self.get_articles(tag=tag)
        context = {"tag": tag, "articles": articles}
        return render(request, "article/article_tag_index_page.html", context)

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for article in self.get_articles():
            # Not tags.append() because we don't want a list of lists
            tags += article.get_tags
        tags = sorted(set(tags))
        return tags


class ArticlePage(Page):
    """Article pages that are restricted to be created within ArticleIndexPage."""

    article_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    date_published = models.DateField("Date article published", blank=True, null=True)

    categories = ParentalManyToManyField("article.ArticleCategory", blank=True)

    body = StreamField(
        BaseStreamBlock(), verbose_name="Article body", blank=True, use_json_field=True
    )

    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    # Specifies that these pages can only be created with ArticleIndexPage types.
    parent_page_types = ['ArticleIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("article_image"),
        InlinePanel(
            "article_person_relationship", label="Author(s)", panels=None, min_num=1
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        FieldPanel("date_published"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

    def get_context(self, request):
        context = super(ArticlePage, self).get_context(request)
        context["tags"] = self.tags.all().order_by("name")
        return context
