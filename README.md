# How to use

## Install

After cloning this repo to your computer, go to the directory where `setup.py` resides and use the following command to install the pacakge:

```bash
pip install -e ./
```

## Download data

The pacakge relies on a pre-calculated data frame that needs to be downloaded.
You can use the following command in a Python console or notebook:

```py
import vMFD
vMFD.download_data("word_moral_appeals_googlenews")
```

You can replace `word_moral_appeals_googlenews` with other categories. Currently the following categories are supported:

| Category name | Note |
|---------------|------|
| word_moral_appeals_googlenews    | Based on pretrained embedding by Google. The embedding contains 300-dimensional vectors for 3 million words and phrases. See https://code.google.com/archive/p/word2vec/ for details. |

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
