import json

with open('src/01_generate_dim_data.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'MultiTableMetadata()' in "".join(cell.get('source', [])):
        source = [
            "df_prod_seed = pd.read_excel('../templates/MauFileSanPham.xlsx', header=0)\n",
            "df_cust_seed = pd.read_excel('../templates/MauFileKhachHang.xlsx', sheet_name='CustomerTemplate', header=0)\n",
            "df_empl_seed = pd.read_excel('../templates/MauFileImportNhanVien.xlsx', header=0)\n",
            "\n",
            "metadata = MultiTableMetadata()\n",
            "metadata.detect_from_dataframes(data={\n",
            "    'DIM_PRODUCTS': df_prod_seed,\n",
            "    'DIM_CUSTOMERS': df_cust_seed,\n",
            "    'DIM_EMPLOYEES': df_empl_seed\n",
            "})\n",
            "\n",
            "# Cập nhật Primary Key\n",
            "metadata.update_table(table_name='DIM_PRODUCTS', primary_key='Mã hàng')\n",
            "metadata.update_table(table_name='DIM_CUSTOMERS', primary_key='Mã khách hàng')\n",
            "metadata.update_table(table_name='DIM_EMPLOYEES', primary_key='Mã nhân viên')\n",
            "\n",
            "# Cập nhật sdtype cho các cột cụ thể\n",
            "metadata.update_column(table_name='DIM_PRODUCTS', column_name='Mã hàng', sdtype='id')\n",
            "metadata.update_column(table_name='DIM_PRODUCTS', column_name='Tên hàng', sdtype='categorical')\n",
            "metadata.update_column(table_name='DIM_PRODUCTS', column_name='Thương hiệu', sdtype='categorical')\n",
            "\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Mã khách hàng', sdtype='id')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Tên khách hàng', sdtype='person_name')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Điện thoại', sdtype='phone_number')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Địa chỉ', sdtype='address')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Loại khách', sdtype='categorical')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Khu vực giao hàng', sdtype='categorical')\n",
            "metadata.update_column(table_name='DIM_CUSTOMERS', column_name='Phường/Xã', sdtype='categorical')\n",
            "\n",
            "metadata.update_column(table_name='DIM_EMPLOYEES', column_name='Mã nhân viên', sdtype='id')\n",
            "metadata.update_column(table_name='DIM_EMPLOYEES', column_name='Tên nhân viên (*)', sdtype='person_name')\n",
            "metadata.update_column(table_name='DIM_EMPLOYEES', column_name='Số điện thoại (*)', sdtype='phone_number')\n",
            "metadata.update_column(table_name='DIM_EMPLOYEES', column_name='Loại lương', sdtype='categorical')\n",
            "metadata.update_column(table_name='DIM_EMPLOYEES', column_name='Chức danh', sdtype='categorical')\n",
            "\n",
            "print(\"Multi-table Metadata initialized with detect_from_dataframes.\")"
        ]
        cell['source'] = source
        cell['outputs'] = [] # Clean error outputs

with open('src/01_generate_dim_data.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated.")
