import pandas as pd
from sdv.metadata import MultiTableMetadata

df1 = pd.DataFrame({'id':[1], 'Email':['a@b.c']})
df2 = pd.DataFrame({'id':[2], 'Email':['b@c.d']})
m = MultiTableMetadata()
m.detect_from_dataframes({'T1': df1, 'T2': df2})

d = m.to_dict()
d['relationships'] = []
m2 = MultiTableMetadata.load_from_dict(d)
print(m2.relationships)
