from django import forms

class UploadForm(forms.Form):
    file_path1 = forms.FileField(label='File Path 1', required=True)
    file_path2 = forms.FileField(label='File Path 2', required=True)
    file_path3 = forms.FileField(label='File Path 3', required=True)
    file_path4 = forms.FileField(label='File Path 4', required=True)
