import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from classifier.models import Email
from classifier.readers.csv_reader import CSVByteReader

from .forms import UploadFileForm

logger = logging.getLogger(__name__)


def handle_uploaded_file(f):
    extension = f.name.split(".")[-1]
    if extension == "csv":
        csv_reader = CSVByteReader(f)
        data = csv_reader.read_as_list_of_dicts()

        chunk_size = 1000
        for i in range(0, len(data), chunk_size):
            emails = []
            chunk = data[i : i + chunk_size]
            for row in chunk:
                emails.append(Email(content=row["text"]))

            Email.objects.bulk_create(emails)

    elif extension == "json":
        # TODO: Implement JSON reader
        pass
    elif extension == "xml":
        # TODO: Implement XML reader
        pass


def upload_file_view(request):
    if request.method == "POST":
        logger.info("Upload data file initiated")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["data_file"])
            logger.info("File uploaded successfully")

            return HttpResponseRedirect("/admin/classifier/email/")

        logger.warning("File upload failed")

        return render(request, "admin/upload_form.html", {"form": form})
    else:
        form = UploadFileForm()
    return render(request, "admin/upload_form.html", {"form": form})
