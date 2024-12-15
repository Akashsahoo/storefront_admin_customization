from django.contrib import admin,messages

from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode
from .models import Collection,Product,Customer,Order,OrderItem
from tags.models import TaggedItem
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self,request,model_admin):
        return [
            ('<10','Low')
        ]

    def queryset(self,request,queryset):
        if  self.value() == '<10':
            return queryset.filter(inventory__lt=10)






@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title','slug']
    # exclude = ['promotions']
    #readonly_fields = ['title']
    # prepopulated_fields = {
    #     'slug': ['title']  inlines = [TagInline]
    # }

    autocomplete_fields = ['collection']
    actions = ['clear_inventory']

    list_display = ['title','unit_price','inventory_status','collection_title']
    search_fields = ['title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were sucessfully updated'
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']






class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id':str(collection.id)})
        return format_html('<a href="{}">{}</a>',url,collection.products_count)


    def get_queryset(self,request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
