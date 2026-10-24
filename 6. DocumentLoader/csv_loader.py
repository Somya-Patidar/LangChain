from langchain_core.document_loaders import CSVLoader

# Create 1 doc per row
loader = CSVLoader(file_path='Social_Network_Ads.csv')

docs = loader.load()

print(len(docs))
print(docs[1])