# Django-Social-Share

A Django package providing template tags for social media sharing links (Facebook, X/Twitter, LinkedIn, WhatsApp, Telegram, Reddit, Pinterest) and clipboard copying.

---

## Installation

```bash
pip install git+https://github.com/djangomango/django-social-share.git@0.1.0
```

Or add to your `requirements.txt`:

```txt
git+https://github.com/djangomango/django-social-share.git@0.1.0
```

Add `django_social_share` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_social_share",
    ...
]
```

Ensure `django.template.context_processors.request` is in `TEMPLATES` context processors:

```python
TEMPLATES = [
    {
        "OPTIONS": {
            "context_processors": [
                ...
                "django.template.context_processors.request",
            ],
        },
    },
]
```

---

## Usage

### 1. Snippet Template Tags

Load the `social_share` library in your templates. Snippet tags render ready-to-use HTML anchor tags:

```html
{% load social_share %}

<!-- Post to X / Twitter -->
{% post_to_twitter "Check out {{ object.title }}!" object_or_url "Share on X" %}

<!-- Post to Facebook -->
{% post_to_facebook object_or_url "Share on Facebook" %}

<!-- Post to LinkedIn -->
{% post_to_linkedin object_or_url %}

<!-- Post to WhatsApp -->
{% post_to_whatsapp object_or_url "Share via WhatsApp" %}

<!-- Post to Telegram -->
{% post_to_telegram "Check out {{ object.title }}" object_or_url %}

<!-- Post to Reddit -->
{% post_to_reddit "Check out {{ object.title }}" object_or_url %}

<!-- Copy to Clipboard -->
{% copy_to_clipboard object_or_url "Copy Link" %}
{% add_copy_script %}
```

### 2. URL-Only Context Tags

If you prefer building your own custom HTML markup, use context tags to retrieve just the sharing URL:

```html
{% post_to_twitter_url "Check out {{ object.title }}!" object_or_url %}
<a href="{{ tweet_url }}" target="_blank" rel="noopener">Custom Tweet Button</a>

{% post_to_facebook_url object_or_url %}
<a href="{{ facebook_url }}" target="_blank" rel="noopener">Custom Facebook Button</a>

{% post_to_whatsapp_url object_or_url %}
<a href="{{ whatsapp_url }}" target="_blank" rel="noopener">Custom WhatsApp Button</a>
```

---

## License & Credits

- Licensed under the **MIT License**.
- Originally created by [Flavio Curella](https://github.com/fcurella/django-social-share).
