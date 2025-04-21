from django.contrib import admin
from workspace.models import Workspace, WorkspaceInvitation
# Register your models here.

admin.site.register(Workspace)
admin.site.register(WorkspaceInvitation)