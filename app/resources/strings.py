"""Text and templates for messages."""

from typing import Any, Protocol, cast

from mako.lookup import TemplateLookup


class FormatTemplate(Protocol):
    """
    Protocol for correct templates typing.
    Allow use format() instead of render() method that needed to maintain consistency
    with regular string formatting.
    """

    def format(self, **kwargs: Any) -> str:  # noqa: WPS125 A003
        """Render template."""


class TemplateFormatterLookup(TemplateLookup):  # type: ignore
    """Represent a collection of templates from the local filesystem."""

    def get_template(self, uri: str) -> FormatTemplate:
        """Cast default mako template to FormatTemplate."""

        def _format(**kwargs: Any) -> str:  # noqa: WPS430
            return cast(str, template.render(**kwargs).rstrip())

        template = super().get_template(uri)
        template.format = _format  # noqa: WPS125
        return cast(FormatTemplate, template)


lookup = TemplateFormatterLookup(
    directories=["app/resources/templates"],
    input_encoding="utf-8",
    strict_undefined=True,
)

HELP_COMMAND_MESSAGE_TEMPLATE = lookup.get_template("help.txt.mako")
