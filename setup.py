#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="simple-vendor-matching-webhook-python",
    description="Example Rossum webhook extension with simple vendor matching",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://developers.rossum.ai/",
    author="Rossum developers",
    author_email="support@rossum.ai",
    license="MIT",
    project_urls={
        "Source": "https://github.com/rossumai/simple-vendor-matching-webhook-python",
        "Tracker": "https://github.com/rossumai/simple-vendor-matching-webhook-python/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests*",)),
    install_requires=["flask", "Werkzeug"],
    python_requires=">=3.6",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-flask"],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "simple_vendor_matching_webhook_python "
            "= simple_vendor_matching_webhook_python.app:entry_point"
        ]
    },
)
