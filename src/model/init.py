import os
import gdown

def download_model(url, output):
    if os.path.isfile(output):
        return
    gdown.download(url, output, quiet=True)
