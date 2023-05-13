from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import (
    ImageGridBlock,
    SingleColumnBlock,
    TwoColumnBlock,
    ThreeColumnBlock,
    FourColumnBlock,
    HeroImageBlock,
)


class StandardPage(Page):
    body = StreamField(
        [
            ("hero_image", HeroImageBlock(icon="image")),
            ("single_column", SingleColumnBlock(group="COLUMNS")),
            ("two_columns", TwoColumnBlock(group="COLUMNS")),
            ("three_columns", ThreeColumnBlock(group="COLUMNS")),
            ("four_columns", FourColumnBlock(group="COLUMNS")),
            (
                "image_grid",
                ImageGridBlock(
                    icon="image",
                    min_num=2,
                    max_num=4,
                    help_text="Minimum 2 blocks and a maximum of 4 blocks",
                ),
            ),
        ],
        use_json_field=True,
        default="",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
