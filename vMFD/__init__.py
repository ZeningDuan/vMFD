import logging
import pandas as pd
import os
import urllib.request
import errno


def get_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)
    # Create handlers
    handler = logging.StreamHandler()
    # Create formatters and add it to handlers
    logger_format = logging.Formatter("%(asctime)s@%(name)s:%(levelname)s: %(message)s")
    handler.setFormatter(logger_format)
    # Add handlers to the logger
    logger.addHandler(handler)
    # Set level
    level = logging.getLevelName("INFO")
    logger.setLevel(level)
    return logger


logger = get_logger(__name__)

package_directory = os.path.dirname(os.path.abspath(__file__))
package_root_directory = os.path.dirname(package_directory)
local_dataset_directory = os.path.join(package_directory, "data")


################################################################################
################################################################################
# vMFD class
################################################################################
class vMFD:
    MF_FILES = {
        "word_moral_appeals_googlenews": {
            "note": """Moral appeals based on pretrained embedding by Google.
                Contains 300-dimensional vectors for 3 million words and phrases based on Google News dataset.
                See https://code.google.com/archive/p/word2vec/ for details.
                """,
            "url": "https://raw.githubusercontent.com/yang3kc/VecOpt/main/vMFD/data/word_moral_googlenews.csv.gz",
            "filename": "word_moral_googlenews.csv.gz",
        }
    }
    MF_categories = ["care", "authority", "fairness", "loyalty", "sanctity"]

    def __init__(self, moral_fundation_version="word_moral_appeals_googlenews"):
        if moral_fundation_version not in self.MF_FILES:
            logger.error(
                f"""Moral appeal data from {moral_fundation_version} does not exist.
                    Choose one from {list(self.MF_FILES.keys())}"""
            )
            return
        mf_path = os.path.join(
            local_dataset_directory, self.MF_FILES[moral_fundation_version]["filename"]
        )
        if not os.path.isfile(mf_path):
            logger.error(
                f"""Moral appeal data for {moral_fundation_version} not found!
                Please download it using the following python function:

                vMFD.download_data("word_moral_appeals_googlenews")

                'word_moral_appeals_googlenews' can be replaced with other categories in {list(self.MF_FILES.keys())}

                Remember to create a new instance of the vMFD class after you successfully download the moral appeal data.
                """
            )
            return
        logger.info(f"Loading {mf_path}")
        mf_df = pd.read_csv(mf_path)
        mf_df = mf_df[mf_df["word"].notna()]
        logger.info(f"Converting data frame to dict")
        mf_df.set_index("word", inplace=True)
        self.mf_dict = mf_df.to_dict("index")

    def _preprocess_doc(self, doc):
        # Lower case the doc?
        return str(doc).split(" ")

    def _get_doc_mf_df(self, doc):
        doc_words = self._preprocess_doc(doc)
        word_mfs = []
        for doc_word in doc_words:
            word_mf = self.mf_dict.get(doc_word)
            if word_mf:
                word_mfs.append(word_mf)
        return pd.DataFrame.from_records(word_mfs)

    def calculate_valence(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return dict(dat.mean())

    def calculate_positivity(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return dict((dat * (dat > 0)).abs().mean())

    def calculate_negativity(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return dict((dat * (dat < 0)).abs().mean())

    def calculate_strength(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return dict(dat.abs().mean())

    def calculate_ambivalence(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return dict(dat.var(ddof=0))

    def calculate_metrics(self, doc):
        doc_mf_df = self._get_doc_mf_df(doc)
        dat = doc_mf_df[self.MF_categories]
        return {
            "valence": dict(dat.mean()),
            "positivity": dict((dat * (dat > 0)).abs().mean()),
            "negativity": dict((dat * (dat < 0)).abs().mean()),
            "strength": dict(dat.abs().mean()),
            "polarity": dict(dat.var(ddof=0)),
        }


################################################################################
################################################################################
# Paths related
################################################################################
def _makedirs(path):
    """
    Create a new directory on the disk
    Input:
        path::string:  target directory
    """
    try:
        os.makedirs(os.path.expanduser(os.path.normpath(path)))
    except OSError as e:
        if e.errno != errno.EEXIST and os.path.isdir(path):
            raise e


def _download_url(url, folder, log=True, file_name=None):
    """Downloads the content of an URL to a folder.
    Input:
        url::string:      target url
        folder::string:   target folder
        log::bool:        weather to log the information
        file_name:string: file_name for the target file
    Retrun:
        path::string: the path of the content
    """

    if file_name is None:
        file_name = url.rpartition("/")[2]
    path = os.path.join(folder, file_name)

    if os.path.exists(path):  # pragma: no cover
        if log:
            logger.info("File exsits: {}".format(file_name))
        return path

    if log:
        logger.info("Downloading: {}".format(url))

    _makedirs(folder)

    # Faking the request headers to bypass some download restrictions
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    req = urllib.request.Request(url, headers=hdr)
    data = urllib.request.urlopen(req)

    with open(path, "wb") as f:
        f.write(data.read())

    return path


def download_data(moral_fundation_version=""):
    if moral_fundation_version not in vMFD.MF_FILES:
        logger.error(
            f"""Moral appeal data for {moral_fundation_version} does not exist.
                Choose one from {list(vMFD.MF_FILES.keys())}"""
        )
        return

    _download_url(
        vMFD.MF_FILES[moral_fundation_version]["url"],
        local_dataset_directory,
        file_name=vMFD.MF_FILES[moral_fundation_version]["filename"],
    )

    logger.info("Data downloaded!")
