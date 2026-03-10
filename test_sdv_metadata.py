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

# Cập nhật Primary Key
metadata.set_primary_key(table_name='DIM_PRODUCTS', column_name='Mã hàng')
metadata.set_primary_key(table_name='DIM_CUSTOMERS', column_name='Mã khách hàng')
metadata.set_primary_key(table_name='DIM_EMPLOYEES', column_name='Mã nhân viên')

print("Success")
