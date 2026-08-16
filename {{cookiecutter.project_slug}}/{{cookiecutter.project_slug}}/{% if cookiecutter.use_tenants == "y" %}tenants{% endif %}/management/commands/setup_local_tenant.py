from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from django_template.tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = "Setup initial tenant environment"

    def handle(self, *args, **options):

        User = get_user_model()

        email = "admin@gmail.com"
        password = "Admin@123"

        with transaction.atomic():

            # ---------------------------------
            # 1. Create initial user
            # ---------------------------------

            user, user_created = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": "Admin",
                    "is_active": True,
                },
            )

            if user_created:
                user.set_password(password)
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {email}"
                    )
                )


            # ---------------------------------
            # 2. Create public tenant
            # ---------------------------------

            tenant, tenant_created = Tenant.objects.get_or_create(
                schema_name="public",
                defaults={
                    "name": "Public",
                    "owner": user,
                },
            )

            if tenant_created:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Created public tenant"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Public tenant already exists"
                    )
                )


            # ---------------------------------
            # 3. Create local domains
            # ---------------------------------

            for domain_name in [
                "localhost",
                "127.0.0.1",
            ]:

                domain, domain_created = Domain.objects.get_or_create(
                    domain=domain_name,
                    defaults={
                        "tenant": tenant,
                        "is_primary": domain_name == "localhost",
                    },
                )

                if domain_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created domain: {domain_name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Domain already exists: {domain_name}"
                        )
                    )


        # ---------------------------------
        # Completion message
        # ---------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Tenant setup completed successfully"
            )
        )

        self.stdout.write(
            f"Login: {email}"
        )

        self.stdout.write(
            f"Password: {password}"
        )