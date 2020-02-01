
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from pdfminer.pdfpage import PDFPage
import PyPDF2
import os

def convert_pdf(file):
    read_pdf = PyPDF2.PdfFileReader(file)
    page_text = ''
    for i in range(read_pdf.getNumPages()):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        print(page_content)
        page_text += '\n' + page_content

    rv = '\n'.join(i for i in page_text.split('\n'))
    return rv






'''
>>> import os
>>> from application import *
>>> path = os.path.join(os.getcwd(),'test_pdfs','test_file_1.pdf')
>>> convert_pdf(path)


'''
from flask import Flask, send_file, render_template, render_template_string, request, current_app
from wtforms import Form , FileField, SubmitField
import os

class UploadForm(Form):
    upload_file = FileField("Upload File ")
    submit_btn = SubmitField("Submit")


TEMPLATE_STRING = '''
<form method="post" enctype="multipart/form-data">
<div class='row'>

{{ form.upload_file.label }}
{{ form.upload_file() }}

{{form.submit_btn.label}}
{{ form.submit_btn() }}
</div>
<form>
'''

print(__name__)
app = Flask(__name__)

def write_file(text, file_name):
    static_folder = current_app.static_folder

    with open(os.path.join(static_folder,'text_files',file_name + '.txt'),'w') as f:
        f.write(text)

@app.route('/',methods=['GET','POST'])
def index():
    form = UploadForm()
    if  request.method == 'POST':
        print(current_app.static_folder)
        file = request.files['upload_file']
        text = convert_pdf(file )
        print(file )

        dir_path = os.path.dirname(os.path.realpath(__file__))
        static_path = current_app.static_folder
        if not os.path.isdir(os.path.join(static_path, 'text_files')):
            os.mkdir(os.path.join(static_path,'text_files'))
        expected_filename = file.filename.split('.')[0]+'.txt'
        write_file(text, expected_filename)
        print(" At POST Method")
    return render_template_string(TEMPLATE_STRING , form=form)

if __name__ == '__main__':
    app.secret_key = "secret"
    app.run(debug=True)
