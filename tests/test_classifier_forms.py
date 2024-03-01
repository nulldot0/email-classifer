import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from classifier.forms import UploadFileForm


@pytest.mark.django_db
def test_clean_data_file_with_valid_csv():
    csv_content = b"text,another_column\nvalue1,value2\nvalue3,value4"
    csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

    form = UploadFileForm(files={"data_file": csv_file})
    assert form.is_valid(), form.errors.as_text()


@pytest.mark.django_db
def test_clean_data_file_with_invalid_csv():
    csv_content = b"wrong_column,another_column\nvalue1,value2\nvalue3,value4"
    csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

    form = UploadFileForm(files={"data_file": csv_file})
    assert not form.is_valid()
    assert "text" in form.errors.as_text()


@pytest.mark.django_db
def test_clean_data_file_with_unsupported_file_type():
    txt_content = b"Just some text"
    txt_file = SimpleUploadedFile("test.txt", txt_content, content_type="text/plain")

    form = UploadFileForm(files={"data_file": txt_file})
    assert not form.is_valid()
    assert "File type not supported" in form.errors.as_text()
