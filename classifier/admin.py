from django.contrib import admin

from classifier.models import Email


@admin.action(description="Classify email")
def classify_email(modeladmin, request, queryset):
    Email.bulk_classify_email(queryset)


class EmailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "classification",
        "is_classified",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "classification",
        "is_classified",
    )
    search_fields = (
        "id",
        "classification",
        "is_classified",
    )

    actions = [classify_email]


admin.site.register(Email, EmailAdmin)
