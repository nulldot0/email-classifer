import logging

from django import forms

from classifier.readers.csv_reader import CSVByteReader

logger = logging.getLogger(__name__)


class UploadFileForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        file = self.cleaned_data["data_file"]
        extension = file.name.split(".")[-1]
        if extension not in ["csv", "json", "xml"]:
            raise forms.ValidationError(
                "File type not supported. Please upload a CSV, JSON, or XML file."
            )

        if extension == "csv":
            csv_reader = CSVByteReader(file)
            first_row = csv_reader.read_as_list_of_lists()[0]
            if "text" not in first_row:
                raise forms.ValidationError(
                    "The file does not contain a column with the header `text`."
                )
        elif extension == "json":
            # TODO: Implement JSON reader
            pass
        elif extension == "xml":
            # TODO: Implement XML reader
            pass

        return file
