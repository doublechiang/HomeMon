#!/usr/bin/env python3

import pandas as pd
import database as dblyr
from sqlalchemy.sql import select
import tkinter
import matplotlib.pyplot as plt
plt.matplotlib.use('TkAgg')

# Local import
import temperature

conn = dblyr.Database().getConn()
engine = dblyr.Database().getEngine()
s = select([temperature.Temperature])
df = pd.read_sql(s, conn)
print(df.head())
df.plot(kind='line', x='datetime', y='temp')
plt.show()



