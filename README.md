[![PyPI version](https://badge.fury.io/py/vMFD.svg)](https://badge.fury.io/py/vMFD)

# Introduction

`vMFD` is an easy-to-use Python package for inferring moral appeals from text.
It extends eMFD through word embedding and yields superior performance.

# Quick start

## Install

After cloning this repo to your computer, go to the directory where `setup.py` resides and use the following command to install the package:

```bash
pip install vMFD
```

## Download data

The package relies on a pre-calculated data frame that needs to be downloaded.
You can use the following command in a Python console or notebook:

```py
import vMFD
vMFD.download_data("word_moral_appeals_googlenews")
```

You can replace `word_moral_appeals_googlenews` with other categories. Currently, the following categories are supported:

| Category name | Note |
|---------------|------|
| word_moral_appeals_googlenews    | Based on pre-trained embedding by Google. The embedding contains 300-dimensional vectors for 3 million words and phrases. See https://code.google.com/archive/p/word2vec/ for details. |

## Calculate moral intuitions

Once the data is downloaded, you can calculate the moral intuitions of any text.

```py
import vMFD

vo = vMFD.vMFD()

# Only calculate the valence
vo.calculate_valence("Trump is the best president")

# Calculate all metrics
vo.calculate_metrics("Trump is the best president")
```
