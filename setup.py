from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fp:
    readme = fp.read()

setup(
    name="django-social-share",
    version="0.1.0",
    author="Flavio Curella",
    author_email="flavio.curella@curella.org",
    maintainer="buswedg",
    maintainer_email="buswedg@djangomango.com",
    url="https://github.com/djangomango/django-social-share",
    install_requires=[
        "Django>=4.2",
    ],
    tests_require=[
        "Django>=4.2",
    ],
    test_suite="django_social_share.tests.runtests.runtests",
    license="MIT",
    description="Templatetags for 'tweet this' and 'share on facebook'",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
    ],
    python_requires=">=3.10",
    packages=find_packages(),
    include_package_data=True,
)
