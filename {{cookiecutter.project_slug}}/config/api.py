from ninja import NinjaAPI
from {{ cookiecutter.project_slug }}.users.api.controllers import router as users_router

api = NinjaAPI()

api.add_router("/users", users_router)
