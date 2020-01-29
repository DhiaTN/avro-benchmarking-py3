from setuptools import find_packages, setup

setup(
    name="avro-bench",
    version="0.0.0",
    description="avro tools bechmarking.",
    author="Dhia Abbassi",
    author_email="dhia.absi@gmail.com",
    packages=find_packages(),
    package_dir={"": "."},
    include_package_data=True,
    entry_points={"console_scripts": []},
    zip_safe=False,
    keywords="avro",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
