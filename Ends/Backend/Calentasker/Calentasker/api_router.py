from rest_framework.routers import DefaultRouter

from users.urls import router as users_router
from groups.urls import router as groups_router
from tasks.urls import router as tasks_router

api = DefaultRouter()

user_routes = users_router.registry
group_routes = groups_router.registry
task_routes = tasks_router.registry

api.registry.extend(user_routes)
api.registry.extend(group_routes)
api.registry.extend(task_routes)