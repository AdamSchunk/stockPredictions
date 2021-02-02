import os

def data_path(*args):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rawYahooData")
    return os.path.join(data_dir, *args)

