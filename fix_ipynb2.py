import json

with open('src/01_generate_dim_data.ipynb', 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'update_table' in "".join(cell.get('source', [])):
        source = "".join(cell['source'])
        source = source.replace('metadata.update_table(table_name=', 'metadata.set_primary_key(table_name=')
        cell['source'] = [line + '\n' for line in source.split('\n')]
        # Clean trailing newline in the last element if present
        if cell['source'][-1] == '\n':
            cell['source'].pop()
        else:
            cell['source'][-1] = cell['source'][-1][:-1]
        
        cell['outputs'] = []

with open('src/01_generate_dim_data.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated again.")
