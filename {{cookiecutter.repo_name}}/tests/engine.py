from subprocess import call
from os import path
import hitchpostgres
import hitchselenium
import hitchpython
import hitchserve
import hitchredis
import hitchtest
import hitchsmtp


# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Engine for orchestating and interacting with the app."""

    def set_up(self):
        """Ensure virtualenv present, then run all services."""
        python_package = hitchpython.PythonPackage(
            python_version=self.preconditions['python_version']
        )
        python_package.build()
        python_package.verify()

        call([
            python_package.pip, "install", "-r",
            path.join(PROJECT_DIRECTORY, "requirements/local.txt")
        ])

        postgres_package = hitchpostgres.PostgresPackage(
            version=self.settings["postgres_version"],
        )
        postgres_package.build()
        postgres_package.verify()

        redis_package = hitchredis.RedisPackage(version="2.8.4")
        redis_package.build()
        redis_package.verify()

        self.services = hitchserve.ServiceBundle(
            project_directory=PROJECT_DIRECTORY,
            startup_timeout=float(self.settings["startup_timeout"]),
            shutdown_timeout=5.0,
        )

        postgres_user = hitchpostgres.PostgresUser("{{cookiecutter.repo_name}}", "password")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            postgres_package=postgres_package,
            users=[postgres_user, ],
            databases=[hitchpostgres.PostgresDatabase("{{cookiecutter.repo_name}}", postgres_user), ]
        )

        self.services['HitchSMTP'] = hitchsmtp.HitchSMTPService(port=1025)

        self.services['Django'] = hitchpython.DjangoService(
            python=python_package.python,
            port=8000,
            version=str(self.settings.get("django_version")),
            settings="config.settings.local",
            needs=[self.services['Postgres'], ],
            env_vars=self.settings['environment_variables'],
        )

        self.services['Redis'] = hitchredis.RedisService(
            redis_package=redis_package,
            port=16379,
        )
{% if cookiecutter.celery_support == "y" %}
        self.services['Celery'] = hitchpython.CeleryService(
            python=python_package.python,
            version="3.1.18",
            app="{{cookiecutter.repo_name}}.taskapp", loglevel="INFO",
            needs=[
                self.services['Redis'], self.services['Django'],
            ],
            env_vars=self.settings['environment_variables'],
        )
{% endif %}
        self.services['Firefox'] = hitchselenium.SeleniumService(
            xvfb=self.settings.get("quiet", False),
            no_libfaketime=True,
        )

#        import hitchcron
#        self.services['Cron'] = hitchcron.CronService(
#            run=self.services['Django'].manage("trigger").command,
#            every=1,
#            needs=[ self.services['Django'], ],
#        )

        self.services.startup(interactive=False)

        # Configure selenium driver
        self.driver = self.services['Firefox'].driver
        self.driver.set_window_size(self.settings['window_size']['height'], self.settings['window_size']['width'])
        self.driver.set_window_position(0, 0)
        self.driver.implicitly_wait(2.0)
        self.driver.accept_next_alert = True

    def pause(self, message=None):
        """Stop. IPython time."""
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
        self.ipython(message)
        if hasattr(self, 'services'):
            self.services.stop_interactive_mode()

    def load_website(self):
        """Navigate to website in Firefox."""
        self.driver.get(self.services['Django'].url())

    def click(self, on):
        """Click on HTML id."""
        self.driver.find_element_by_id(on).click()

    def fill_form(self, **kwargs):
        """Fill in a form with id=value."""
        for element, text in kwargs.items():
            self.driver.find_element_by_id(element).send_keys(text)

    def click_submit(self):
        """Click on a submit button if it exists."""
        self.driver.find_element_by_css_selector("button[type=\"submit\"]").click()

    def confirm_emails_sent(self, number):
        """Count number of emails sent by app."""
        assert len(self.services['HitchSMTP'].logs.json()) == int(number)

    def wait_for_email(self, containing=None):
        """Wait for, and return email."""
        self.services['HitchSMTP'].logs.out.tail.until_json(
            lambda email: containing in email['payload'] or containing in email['subject'],
            timeout=25,
            lines_back=1,
        )

    def time_travel(self, days=""):
        """Make all services think that time has skipped forward."""
        self.services.time_travel(days=int(days))

    def on_failure(self):
        """Stop and IPython."""
        if not self.settings['quiet']:
            if self.settings.get("pause_on_failure", False):
                self.pause(message=self.stacktrace.to_template())

    def on_success(self):
        """Pause on success if enabled."""
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def tear_down(self):
        """Shut down services required to run your test."""
        if hasattr(self, 'services'):
            self.services.shutdown()
