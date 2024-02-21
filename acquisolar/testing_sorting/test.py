import searchengine
import server
import classification

doc_dir = './documents'
index_dir = './index_storage'
searchengine.index(doc_dir, index_dir=index_dir)

full_text,_,_=classification.extract_pdf_info('./documents/HR_Clearway_LOI_Fully_Executed.pdf')
print(full_text)









