import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# a function to cast to float and integer datatypes. use for desired columns.
def cast_number(item):
    try:
        # First, try to cast to float
        return float(item) if isinstance(float(item), float) else item
    except (TypeError, ValueError):
        try:
            # If float conversion fails, try casting to int
            return int(item)
        except (TypeError, ValueError):
            return item
    
