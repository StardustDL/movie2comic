import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, "data")

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
