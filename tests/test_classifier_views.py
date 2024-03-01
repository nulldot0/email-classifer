import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from classifier.models import Email
from classifier.views import handle_uploaded_file


@pytest.mark.django_db
def test_upload_file_view(client, tmpdir):
    f = tmpdir.join("test.csv")
    f.write('text\n"Sample email content"')
    csv_file = SimpleUploadedFile(
        f.basename, str(f.read()).encode("utf-8"), content_type="text/csv"
    )
    response = client.post(reverse("upload-data"), {"data_file": csv_file}, follow=True)

    assert response.status_code == 200
    assert Email.objects.count() > 0
    assert Email.objects.first().content == "Sample email content"


@pytest.mark.django_db
def test_handle_uploaded_file(tmpdir):
    f = tmpdir.join("test.csv")
    f.write('text\n"Sample email content"')
    csv_file = SimpleUploadedFile(
        f.basename, str(f.read()).encode("utf-8"), content_type="text/csv"
    )

    handle_uploaded_file(csv_file)

    assert Email.objects.count() > 0
    assert Email.objects.first().content == "Sample email content"


@pytest.mark.django_db
def test_handle_uploaded_file_invalid_csv(client, tmpdir):
    f = tmpdir.join("test.txt")
    f.write('text\n"Sample email content"')
    csv_file = SimpleUploadedFile(
        f.basename, str(f.read()).encode("utf-8"), content_type="text/csv"
    )
    response = client.post(reverse("upload-data"), {"data_file": csv_file}, follow=True)

    assert "File type not supported" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_get_upload_file_view(client):
    response = client.get(reverse("upload-data"))
    assert response.status_code == 200
    assert "form" in response.context
    assert "data_file" in response.context["form"].fields
    assert "Upload" in response.content.decode("utf-8")
    assert "csrfmiddlewaretoken" in response.content.decode("utf-8")
