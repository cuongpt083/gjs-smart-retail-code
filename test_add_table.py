import pandas as pd
from sdv.metadata import MultiTableMetadata, SingleTableMetadata

df_prod_seed = pd.read_excel('templates/MauFileSanPham.xlsx', header=0)
df_cust_seed = pd.read_excel('templates/MauFileKhachHang.xlsx', sheet_name='CustomerTemplate', header=0)
df_empl_seed = pd.read_excel('templates/MauFileImportNhanVien.xlsx', header=0)

pm = SingleTableMetadata()
pm.detect_from_dataframe(df_prod_seed)
cm = SingleTableMetadata()
cm.detect_from_dataframe(df_cust_seed)
em = SingleTableMetadata()
em.detect_from_dataframe(df_empl_seed)

metadata = MultiTableMetadata()
metadata.add_table('DIM_PRODUCTS', metadata=pm)
metadata.add_table('DIM_CUSTOMERS', metadata=cm)
metadata.add_table('DIM_EMPLOYEES', metadata=em)

print(metadata.to_dict())
