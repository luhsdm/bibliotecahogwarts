from usuarios.models import Usuario
from django.contrib import admin

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    def abreviar_nome(self, obj):
        return obj.abreviar_nome()  # Usando o método abreviar_nome definido no modelo Usuario

    list_display = ('abreviar_nome', 'email', 'ativo')  # Substituindo 'nome' por 'abreviar_nome'
    list_editable = ('email',)
    readonly_fields = ('senha',)
    search_fields = ('nome', 'email')
    list_filter = ('ativo',)
