Using Django-RQ
===============

.. index:: django-rq, task queue, background jobs, RQ, Valkey

Django-RQ is a simple task queue system for Django that uses `RQ (Redis Queue) <https://python-rq.org/>`_ and `Valkey <https://valkey.io/>`_ as the message broker. It provides a lightweight alternative to Celery for applications that need background task processing with minimal configuration.

Why Django-RQ?
--------------

Django-RQ offers several advantages:

- **Simplicity**: Minimal configuration required compared to Celery
- **Built-in Monitoring**: Includes RQ Dashboard for real-time queue monitoring
- **Python-native**: Job failures can be inspected directly in Python
- **Valkey Backend**: Uses Valkey, an open-source Redis-compatible data store
- **Development-friendly**: Easy to test with synchronous mode

When to Use Django-RQ vs Celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Use Django-RQ when:**

- You need simple background tasks with minimal configuration
- You want built-in monitoring without additional setup
- You're comfortable with a simpler feature set
- You prefer inspecting job failures in Python

**Use Celery when:**

- You need complex workflows with chains, groups, and chords
- You require advanced routing and scheduling features
- You need multiple broker support (RabbitMQ, etc.)
- Your application demands enterprise-level task processing

Architecture
------------

When ``use_django_rq`` is enabled, your project includes:

**Services:**

- **Valkey**: Redis-compatible data store running on port 6379
- **RQ Worker**: Processes background jobs from queues
- **RQ Scheduler**: Handles scheduled/periodic tasks
- **RQ Dashboard**: Web-based monitoring interface on port 9181

**Queues:**

- ``default``: General purpose tasks (360s timeout)
- ``high``: High-priority tasks (500s timeout)
- ``low``: Low-priority tasks (default timeout)

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Django-RQ uses the following environment variable:

.. code-block:: bash

   # For Docker environments
   VALKEY_URL=valkey://valkey:6379/0

   # For local development (non-Docker)
   VALKEY_URL=valkey://localhost:6379/0

Settings
~~~~~~~~

The following settings are automatically configured in ``config/settings/base.py``:

.. code-block:: python

   RQ_QUEUES = {
       "default": {
           "URL": VALKEY_URL,
           "DEFAULT_TIMEOUT": 360,
       },
       "high": {
           "URL": VALKEY_URL,
           "DEFAULT_TIMEOUT": 500,
       },
       "low": {
           "URL": VALKEY_URL,
       },
   }
   RQ_SHOW_ADMIN_LINK = True

Creating Tasks
--------------

Use the ``@job`` decorator to create background tasks:

.. code-block:: python

   # myapp/tasks.py
   import django_rq

   @django_rq.job
   def send_welcome_email(user_id):
       """Send a welcome email to a new user."""
       from .models import User
       from django.core.mail import send_mail

       user = User.objects.get(id=user_id)
       send_mail(
           "Welcome!",
           f"Hello {user.username}, welcome to our platform!",
           "noreply@example.com",
           [user.email],
       )

Enqueuing Tasks
---------------

Enqueue tasks from your views or other code:

.. code-block:: python

   from .tasks import send_welcome_email

   # Enqueue to default queue
   send_welcome_email.delay(user.id)

   # Enqueue to specific queue
   queue = django_rq.get_queue("high")
   queue.enqueue(send_welcome_email, user.id)

   # Schedule task for later
   from datetime import timedelta
   queue.enqueue_in(timedelta(minutes=10), send_welcome_email, user.id)

Testing Tasks
-------------

For testing, use synchronous mode to avoid async complications:

.. code-block:: python

   # tests/test_tasks.py
   import django_rq
   from myapp.tasks import send_welcome_email

   def test_send_welcome_email(user):
       """Test that welcome email task works."""
       # Get synchronous queue
       queue = django_rq.get_queue("default", is_async=False)

       # Enqueue and execute immediately
       job = queue.enqueue(send_welcome_email, user.id)

       # Verify job completed
       assert job.is_finished
       assert job.result is None

Monitoring with RQ Dashboard
-----------------------------

Access the RQ Dashboard at http://localhost:9181 (or your host:9181 in production).

The dashboard shows:

- Active queues and worker count
- Jobs by state (queued, started, finished, failed)
- Worker status and statistics
- Failed job inspection with tracebacks

Management Commands
-------------------

Django-RQ provides Django management commands:

.. code-block:: bash

   # Start worker manually (not needed with docker-compose)
   python manage.py rqworker default high low

   # Start scheduler manually
   python manage.py rqscheduler

   # Get worker statistics
   python manage.py rqstats

   # Clear all queues
   python manage.py rqenqueue --clear all

Docker Development
------------------

With Docker, all RQ services start automatically:

.. code-block:: bash

   docker compose -f docker-compose.local.yml up

Access:

- **Application**: http://localhost:8000
- **RQ Dashboard**: http://localhost:9181

Services will auto-reload on code changes using ``watchfiles``.

Production Deployment
---------------------

Docker Production
~~~~~~~~~~~~~~~~~

RQ services are included in ``docker-compose.production.yml``:

.. code-block:: bash

   docker compose -f docker-compose.production.yml up

Ensure you set the environment variable:

.. code-block:: bash

   VALKEY_URL=valkey://valkey:6379/0

Heroku
~~~~~~

The ``Procfile`` includes RQ worker and scheduler:

.. code-block:: text

   worker: python manage.py rqworker default high low
   scheduler: python manage.py rqscheduler

Scale workers as needed:

.. code-block:: bash

   heroku ps:scale worker=2

Best Practices
--------------

1. **Keep tasks focused**: Each task should do one thing well
2. **Use timeouts**: Set appropriate timeouts for long-running tasks
3. **Handle failures gracefully**: Tasks may fail and retry
4. **Log appropriately**: Use Python logging for debugging
5. **Test synchronously**: Use ``is_async=False`` in tests
6. **Choose queues wisely**: Use ``high`` for critical tasks, ``low`` for background cleanup

Example: Image Processing Task
-------------------------------

Here's a complete example of an image processing task:

.. code-block:: python

   # myapp/tasks.py
   import logging
   import django_rq
   from PIL import Image
   from django.core.files.storage import default_storage

   logger = logging.getLogger(__name__)

   @django_rq.job('high', timeout=300)
   def generate_thumbnail(photo_id):
       """Generate thumbnail for uploaded photo."""
       from .models import Photo

       try:
           photo = Photo.objects.get(id=photo_id)

           # Open original image
           img_path = photo.original.path
           img = Image.open(img_path)

           # Generate thumbnail
           img.thumbnail((200, 200))

           # Save thumbnail
           thumb_path = f"thumbnails/{photo_id}.jpg"
           with default_storage.open(thumb_path, 'wb') as f:
               img.save(f, 'JPEG', quality=85)

           # Update model
           photo.thumbnail = thumb_path
           photo.save()

           logger.info(f"Generated thumbnail for photo {photo_id}")

       except Photo.DoesNotExist:
           logger.error(f"Photo {photo_id} not found")
           raise
       except Exception as e:
           logger.exception(f"Failed to generate thumbnail: {e}")
           raise

   # views.py
   from django.views.generic import CreateView
   from .models import Photo
   from .tasks import generate_thumbnail

   class PhotoUploadView(CreateView):
       model = Photo
       fields = ['title', 'original']

       def form_valid(self, form):
           response = super().form_valid(form)
           # Enqueue thumbnail generation in background
           generate_thumbnail.delay(self.object.id)
           return response

Troubleshooting
---------------

Workers Not Processing Jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check that workers are running:

.. code-block:: bash

   docker compose -f docker-compose.local.yml ps

Verify Valkey connection:

.. code-block:: bash

   docker compose -f docker-compose.local.yml exec django python manage.py shell
   >>> import django_rq
   >>> queue = django_rq.get_queue()
   >>> print(queue.connection)

Jobs Failing Silently
~~~~~~~~~~~~~~~~~~~~~

Check failed job queue in RQ Dashboard or via shell:

.. code-block:: python

   import django_rq
   from rq.registry import FailedJobRegistry

   queue = django_rq.get_queue()
   registry = FailedJobRegistry(queue=queue)

   for job_id in registry.get_job_ids():
       job = queue.fetch_job(job_id)
       print(f"Job {job_id}: {job.exc_info}")

Dashboard Not Loading
~~~~~~~~~~~~~~~~~~~~~

Ensure port 9181 is exposed and dashboard service is running:

.. code-block:: bash

   docker compose -f docker-compose.local.yml logs rqdashboard

Further Reading
---------------

- `Django-RQ Documentation <https://github.com/rq/django-rq>`_
- `RQ Documentation <https://python-rq.org/>`_
- `Valkey Documentation <https://valkey.io/>`_
- :doc:`/4-guides/using-celery` - Alternative task queue guide
