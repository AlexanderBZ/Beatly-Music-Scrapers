import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import random
import pandas as pd
import numpy as np
import time
import requests_cache
import boto3
from seo import get_xml

# Beats Per Initial
def updateSeo(beatly_data):    
    s3 = boto3.client('s3', aws_access_key_id="AKIA4I2FAJL2DF4NZTFE", aws_secret_access_key="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")
    #s3.download_file('beatlymusicseo', 'beatly_data.xml', 'beatly_data.xml')
    get_xml.getData(beatly_data)

    with open("beatly_data.xml", "rb") as f:
        s3.upload_fileobj(f, "beatlymusicseo", "beatly_data.xml")