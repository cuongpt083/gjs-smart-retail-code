from sdv.metadata import MultiTableMetadata
metadata = MultiTableMetadata()
# Just trying to see if 'name' is valid
try:
    metadata._validate_sdtype('name')
    print("name is valid")
except Exception as e:
    print(e)
try:
    metadata._validate_sdtype('person_name')
    print("person_name is valid")
except Exception as e:
    print(e)
