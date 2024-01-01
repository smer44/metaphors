from striprtf.striprtf import rtf_to_text

filename = "E:\data\Научная фантастика\Русская\Александр Абашели\Абашели - Женщина в зеркале.rtf"

encoding =   'cp1251'

with (open(filename, 'r', encoding=encoding) as file):
    rtf_text = file.read()
    text = rtf_to_text(rtf_text)
    print(text)




