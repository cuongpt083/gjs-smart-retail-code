import pandas as pd
from sdv.metadata import MultiTableMetadata

df_prod_seed = pd.read_excel('templates/MauFileSanPham.xlsx', header=0)
df_cust_seed = pd.read_excel('templates/MauFileKhachHang.xlsx', sheet_name='CustomerTemplate', header=0)
df_empl_seed = pd.read_excel('templates/MauFileImportNhanVien.xlsx', header=0)

metadata = MultiTableMetadata()
metadata.detect_from_dataframes(data={
    'DIM_PRODUCTS': df_prod_seed,
    'DIM_CUSTOMERS': df_cust_seed,
    'DIM_EMPLOYEES': df_empl_seed
})
rels = metadata.to_dict().get('relationships', [])
print("Dict rels:", rels)
