import re
from typing import Any

from django import template
from django.db.models import Model
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

try:
    from django_bitly.templatetags.bitly import bitlify

    DJANGO_BITLY = True
except ImportError:
    DJANGO_BITLY = False


register = template.Library()

BITLY_REGEX = re.compile(r"^https?://bit\.ly/")


def compile_text(context: Any, text: str) -> str:
    """Render string template with given context."""
    ctx = template.context.Context(context)
    return str(template.Template(text).render(ctx))


def _build_url(request: Any, obj_or_url: Any) -> str:
    """Build absolute URI from model object or raw URL string."""
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            if DJANGO_BITLY:
                url = bitlify(obj_or_url)
                if not BITLY_REGEX.match(url):
                    return str(
                        request.build_absolute_uri(obj_or_url.get_absolute_url())
                    )
                return str(url)
            return str(request.build_absolute_uri(obj_or_url.get_absolute_url()))
        return str(request.build_absolute_uri(obj_or_url))
    return ""


def _compose_tweet(text: str, url: str | None = None) -> str:
    """Compose tweet text truncated to Twitter character limits."""
    twitter_max_number_of_characters = 140
    twitter_link_length = 23

    url_length = len(" ") + twitter_link_length if url else 0
    total_length = len(text) + url_length

    if total_length > twitter_max_number_of_characters:
        text = f"{text[: (twitter_max_number_of_characters - url_length - 1)]}…"

    return f"{text} {url}" if url else text


@register.simple_tag(takes_context=True)
def post_to_twitter_url(context: Any, text: str, obj_or_url: Any = None) -> Any:
    """Generate Twitter share URL and store it in template context."""
    text = compile_text(context, text)
    request = context["request"]

    url = _build_url(request, obj_or_url)

    tweet = _compose_tweet(text, url)
    context["tweet_url"] = f"https://twitter.com/intent/tweet?text={urlencode(tweet)}"
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_twitter.html", takes_context=True
)
def post_to_twitter(
    context: Any,
    text: str,
    obj_or_url: Any = None,
    link_text: str = "",
    link_class: str = "",
) -> Any:
    """Render Twitter share button markup."""
    context = post_to_twitter_url(context, text, obj_or_url)

    request = context["request"]
    url = _build_url(request, obj_or_url)
    tweet = _compose_tweet(text, url)

    context["link_class"] = link_class
    context["link_text"] = link_text or "Post to Twitter"
    context["full_text"] = tweet
    return context


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context: Any, obj_or_url: Any = None) -> Any:
    """Generate Facebook share URL and store it in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["facebook_url"] = (
        f"https://www.facebook.com/sharer/sharer.php?u={urlencode(url)}"
    )
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_facebook.html", takes_context=True
)
def post_to_facebook(
    context: Any, obj_or_url: Any = None, link_text: str = "", link_class: str = ""
) -> Any:
    """Render Facebook share button markup."""
    context = post_to_facebook_url(context, obj_or_url)
    context["link_class"] = link_class or ""
    context["link_text"] = link_text or "Post to Facebook"
    return context


@register.simple_tag(takes_context=True)
def post_to_gplus_url(context: Any, obj_or_url: Any = None) -> Any:
    """Generate Google+ share URL and store it in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["gplus_url"] = f"https://plus.google.com/share?url={urlencode(url)}"
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_gplus.html", takes_context=True
)
def post_to_gplus(
    context: Any, obj_or_url: Any = None, link_text: str = "", link_class: str = ""
) -> Any:
    """Render Google+ share button markup."""
    context = post_to_gplus_url(context, obj_or_url)
    context["link_class"] = link_class
    context["link_text"] = link_text or "Post to Google+"
    return context


@register.simple_tag(takes_context=True)
def send_email_url(
    context: Any, subject: str, text: str, obj_or_url: Any = None
) -> Any:
    """Generate mailto URL with subject and body in template context."""
    text = compile_text(context, text)
    subject = compile_text(context, subject)
    request = context["request"]
    url = _build_url(request, obj_or_url)
    full_text = f"{text} {url}"
    context["mailto_url"] = (
        f"mailto:?subject={urlencode(subject)}&body={urlencode(full_text)}"
    )
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/send_email.html", takes_context=True
)
def send_email(
    context: Any,
    subject: str,
    text: str,
    obj_or_url: Any = None,
    link_text: str = "",
    link_class: str = "",
) -> Any:
    """Render email share button markup."""
    context = send_email_url(context, subject, text, obj_or_url)
    context["link_class"] = link_class
    context["link_text"] = link_text or "Share via email"
    return context


@register.filter(name="linkedin_locale")
def linkedin_locale(value: str) -> str:
    """Convert hyphenated locale to LinkedIn underscore format."""
    if "-" not in value:
        return value

    lang, country = value.split("-")
    return f"{lang}_{country.upper()}"


@register.simple_tag(takes_context=True)
def post_to_linkedin_url(context: Any, obj_or_url: Any = None) -> Any:
    """Generate LinkedIn share URL and store it in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["linkedin_url"] = url
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_linkedin.html", takes_context=True
)
def post_to_linkedin(context: Any, obj_or_url: Any = None, link_class: str = "") -> Any:
    """Render LinkedIn share button markup."""
    context = post_to_linkedin_url(context, obj_or_url)
    context["link_class"] = link_class
    return context


@register.simple_tag(takes_context=True)
def post_to_reddit_url(context: Any, title: str, obj_or_url: Any = None) -> Any:
    """Generate Reddit share URL and store it in template context."""
    request = context["request"]
    title = compile_text(context, title)
    url = _build_url(request, obj_or_url)
    context["reddit_url"] = mark_safe(
        f"https://www.reddit.com/submit?title={urlencode(title)}&url={urlencode(url)}"
    )
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_reddit.html", takes_context=True
)
def post_to_reddit(
    context: Any,
    title: str,
    obj_or_url: Any = None,
    link_text: str = "",
    link_class: str = "",
) -> Any:
    """Render Reddit share button markup."""
    context = post_to_reddit_url(context, title, obj_or_url)
    context["link_class"] = link_class
    context["link_text"] = link_text or "Post to Reddit"
    return context


@register.simple_tag(takes_context=True)
def post_to_telegram_url(context: Any, title: str, obj_or_url: Any = None) -> Any:
    """Generate Telegram share URL and store it in template context."""
    request = context["request"]
    title = compile_text(context, title)
    url = _build_url(request, obj_or_url)
    context["telegram_url"] = mark_safe(
        f"https://t.me/share/url?text={urlencode(title)}&url={urlencode(url)}"
    )
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_telegram.html", takes_context=True
)
def post_to_telegram(
    context: Any,
    title: str,
    obj_or_url: Any = None,
    link_text: str = "",
    link_class: str = "",
) -> Any:
    """Render Telegram share button markup."""
    context = post_to_telegram_url(context, title, obj_or_url)
    context["link_class"] = link_class
    context["link_text"] = link_text or "Post to Telegram"
    return context


@register.simple_tag(takes_context=True)
def post_to_whatsapp_url(context: Any, obj_or_url: Any = None) -> Any:
    """Generate WhatsApp share URL and store it in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["whatsapp_url"] = f"https://api.whatsapp.com/send?text={urlencode(url)}"
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/post_to_whatsapp.html", takes_context=True
)
def post_to_whatsapp(
    context: Any, obj_or_url: Any = None, link_text: str = "", link_class: str = ""
) -> Any:
    """Render WhatsApp share button markup."""
    context = post_to_whatsapp_url(context, obj_or_url)
    context["link_class"] = link_class
    context["link_text"] = link_text or "Post to WhatsApp"
    return context


@register.simple_tag(takes_context=True)
def save_to_pinterest_url(context: Any, obj_or_url: Any = None) -> Any:
    """Generate Pinterest pin URL and store it in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["pinterest_url"] = (
        f"https://www.pinterest.com/pin/create/button/?url={urlencode(url)}"
    )
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/save_to_pinterest.html", takes_context=True
)
def save_to_pinterest(
    context: Any, obj_or_url: Any = None, pin_count: bool = False, link_class: str = ""
) -> Any:
    """Render Pinterest save button markup."""
    context = save_to_pinterest_url(context, obj_or_url)
    context["link_class"] = link_class
    context["pin_count"] = pin_count
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/pinterest_script.html", takes_context=False
)
def add_pinterest_script() -> None:
    """Include Pinterest JavaScript SDK snippet."""


@register.simple_tag(takes_context=True)
def copy_to_clipboard_url(context: Any, obj_or_url: Any = None) -> Any:
    """Store URL for clipboard copying in template context."""
    request = context["request"]
    url = _build_url(request, obj_or_url)
    context["copy_url"] = url
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/copy_to_clipboard.html", takes_context=True
)
def copy_to_clipboard(
    context: Any, obj_or_url: Any = None, link_text: str = "", link_class: str = ""
) -> Any:
    """Render copy-to-clipboard button markup."""
    context = copy_to_clipboard_url(context, obj_or_url)

    context["link_class"] = link_class
    context["link_text"] = link_text or "Copy to clipboard"
    return context


@register.inclusion_tag(
    "django_social_share/templatetags/copy_script.html", takes_context=False
)
def add_copy_script() -> None:
    """Include clipboard helper JavaScript snippet."""
