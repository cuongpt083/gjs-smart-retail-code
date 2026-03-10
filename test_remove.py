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

while getattr(metadata, 'relationships', None):
    r = metadata.relationships[0]
    # In newer SDV it's drop_relationship ? Or simply empty the list.
    print(r)
    break

# Try dropping
try:
    metadata.relationships = []
    print("set relationships=[] works")
except Exception as e:
    print(e)
    try:
        metadata._relationships = []
        print("set _relationships=[] works")
    except Exception as e2:
        print(e2)

