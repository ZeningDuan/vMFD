from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="vMFD",
    version="0.1",
    description="Infer moral appeals from text",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ZeningDuan/vMFD",
    author="Kai-Cheng Yang <yang3kc@gmail.com>, Zening Duan <zening.duan@wisc.edu>",
    license="MIT",
    packages=["vMFD"],
    install_requires=["pandas"],
)
