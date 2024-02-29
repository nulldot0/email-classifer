import logging
import uuid

from django.db import models

logger = logging.getLogger(__name__)


class Email(models.Model):
    CLASSIFICATION_REGULAR = "regular"
    CLASSIFICATION_NEWSLETTER = "newsletter"
    CLASSIFICATION_CHOICES = [
        (CLASSIFICATION_REGULAR, "Regular"),
        (CLASSIFICATION_NEWSLETTER, "Newsletter"),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content = models.TextField()
    classification = models.CharField(
        max_length=20,
        choices=CLASSIFICATION_CHOICES,
        null=True,
        blank=True,
    )
    is_classified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Email {self.id} ({self.classification})"

    class Meta:
        ordering = ["-created_at"]

    def get_classification(self) -> str:
        newsletter_keywords = ["newsletter", "unsubscribe"]

        for keyword in newsletter_keywords:
            if keyword in self.content.lower():
                return self.CLASSIFICATION_NEWSLETTER

        return self.CLASSIFICATION_REGULAR

    def classify(self) -> None:
        logger.info(f"Email {self.id} is being classified")
        if self.is_classified:
            logger.info(
                f"Email {self.id} is already classified as {self.classification}"
            )
            return False

        self.classification = self.get_classification()
        self.is_classified = True
        self.save()
        logger.info(f"Email {self.id} classified as {self.classification}")

    @staticmethod
    def bulk_classify_email(queryset: "Email") -> None:
        logger.info("Bulk classifying emails")
        chunk_size = 1000
        emails = queryset.filter(is_classified=False)
        emails_count = emails.count()
        logger.info(f"Bulk classifying {emails_count} emails")

        newsletters = []
        regulars = []

        for i in range(0, emails_count, chunk_size):
            chunk = emails[i : i + chunk_size]
            for email in chunk:
                email.is_classified = True
                email.classification = email.get_classification()

                if email.classification == Email.CLASSIFICATION_NEWSLETTER:
                    newsletters.append(email)
                else:
                    regulars.append(email)

        Email.objects.bulk_update(
            newsletters, ["is_classified", "classification"], batch_size=chunk_size
        )
        Email.objects.bulk_update(
            regulars, ["is_classified", "classification"], batch_size=chunk_size
        )

        logger.info(f"Classified {len(newsletters)} emails as newsletters")
        logger.info(f"Classified {len(regulars)} emails as regulars")
        logger.info("Bulk classification complete")
