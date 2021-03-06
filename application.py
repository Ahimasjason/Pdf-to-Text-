
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
from flask import(
    Flask,
    send_file,
    render_template,
    render_template_string,
    request,
    current_app,
    url_for,
    send_from_directory,
    redirect,
)
from wtforms import Form , FileField, SubmitField
import os

class UploadForm(Form):
    upload_file = FileField("Upload File ")
    submit_btn = SubmitField("Submit")


TEMPLATE_STRING = '''
{% for i in files %}
<ul>
<li> {{ i }}
<a href='{{ url_for('download_file', file_name= i,action='view') }}'> View</a>
<a href='{{ url_for('download_file', file_name= i) }}' >Download </a>
</li>
</ul>
{% endfor  %}


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

TEXTFOLDER = 'text_files'

def write_file(text, file_name):
    static_folder = current_app.static_folder

    with open(os.path.join(static_folder,TEXTFOLDER,file_name + '.txt'),'w') as f:
        f.write(text)

def get_all_files():
    static_folder = current_app.static_folder
    path =os.path.join(static_folder,TEXTFOLDER)
    if not os.path.isdir(path):
        return ''
    return os.listdir(path)

@app.route('/',methods=['GET','POST'])
def index():
    form = UploadForm()
    if  request.method == 'POST':
        file = request.files['upload_file']
        if not file:
            print (" No file part found")
            return redirect(request.url)

        file_extension = file.filename.split('.')[-1]
        if file_extension != 'pdf':
            return redirect(request.url)
        text = convert_pdf(file )
        #
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        static_path = current_app.static_folder
        if not os.path.isdir(os.path.join(static_path, TEXTFOLDER)):
            os.mkdir(os.path.join(static_path,TEXTFOLDER))
        expected_filename = file.filename.split('.')[0]+'.txt'
        write_file(text, expected_filename)
    all_txt_file = get_all_files()
    return render_template_string(TEMPLATE_STRING , form=form, files=all_txt_file)

@app.route('/download_file')
def download_file():
    file_name = request.args.get("file_name", None)
    action = request.args.get('action', None)

    if file_name is None :
        raise ValueError(" No file ref provided")
    static_path = current_app.static_folder
    folder = os.path.join(static_path, TEXTFOLDER)
    if not os.path.isdir(folder):
        raise FileNotFoundError(" No folder exist ")
    list_of_files = os.listdir(folder)
    if file_name not in list_of_files :
        raise FileNotFoundError("  Unable to find file ")
    if action == 'view':
        return send_file(os.path.join(folder,file_name))
    return send_file(os.path.join(folder,file_name), as_attachment= True)
    # return send_from_directory(current_app.static_folder,TEXTFOLDER+file_name)

if __name__ == '__main__':
    app.secret_key = "secret"
    app.run(debug=True)
