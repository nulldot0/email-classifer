import pytest

from classifier.models import Email


@pytest.fixture
def email_db_setup(db):
    Email.objects.create(content="Regular email content.")
    Email.objects.create(content="Newsletter email content with unsubscribe word.")


def test_email_str(email_db_setup):
    email = Email.objects.get(content="Regular email content.")
    assert str(email) == f"Email {email.id} ({email.classification})"


def test_get_classification_regular(email_db_setup):
    email = Email.objects.get(content="Regular email content.")
    assert email.get_classification() == Email.CLASSIFICATION_REGULAR


def test_get_classification_newsletter(email_db_setup):
    email = Email.objects.get(content="Newsletter email content with unsubscribe word.")
    assert email.get_classification() == Email.CLASSIFICATION_NEWSLETTER


def test_classify_method_sets_classification(email_db_setup):
    email = Email.objects.get(content="Newsletter email content with unsubscribe word.")
    email.classify()
    assert email.is_classified
    assert email.classification == Email.CLASSIFICATION_NEWSLETTER


def test_classify_method_ignores_already_classified(email_db_setup):
    email = Email.objects.get(content="Newsletter email content with unsubscribe word.")
    email.classify()
    classification_after_first = email.classification
    email.classify()
    assert email.classification == classification_after_first


def test_bulk_classify_email(email_db_setup):
    Email.bulk_classify_email(Email.objects.all())
    assert Email.objects.filter(is_classified=True).count() == Email.objects.count()
    assert Email.objects.filter(classification=Email.CLASSIFICATION_REGULAR).exists()
    assert Email.objects.filter(classification=Email.CLASSIFICATION_NEWSLETTER).exists()
