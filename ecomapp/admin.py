import admin_thumbnails
from django import forms
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from ecomapp.models.shop import Category, CategoryLang, Country,\
                                Brand, Product, ProductLang, Images,\
                                ProductReview, Color, Size, Variants

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _


class CategoryLangInline(admin.TabularInline):
    model = CategoryLang
    extra = 1
    show_change_link = True
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('indented_title',)
    list_per_page = 20
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    inlines = [CategoryLangInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ist_display_links = ('name',)
    list_per_page = 20
    search_fields = ['name', ]


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)


@admin_thumbnails.thumbnail('image_file')
class ProductImagesInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ProductLangInline(admin.TabularInline):
    model = ProductLang
    extra = 1
    show_change_link = True
    prepopulated_fields = {'slug': ('name',)}


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label="Опис", widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name'))
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=ManyToManyWidget(Brand, 'name'))

    class Meta:
        model = Product
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', 'stock')
        import_id_fields = ('name',)
        fields = ('product_id', 'category', 'brand', 'name', 'articul', 'image_url', 'description', 'price', 'old_price', 'available',)
        export_order = ('product_id', 'category', 'articul', 'name', 'price', 'old_price', 'available', 'brand', 'description', 'image_url',)


@admin_thumbnails.thumbnail('image_file')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'image_file']


class ProductAdmin(ImportExportActionModelAdmin):
    resources_class = ProductResource
    list_display = ['id', 'category', 'articul', 'name', 'price', 'stock', 'available', 'created', 'updated', 'image_tag']
    list_display_links = ('articul', 'name',)
    ordering = ['created']
    list_per_page = 50
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    list_filter = ['available', 'created', 'updated']
    readonly_fields = ('image_tag',)
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImagesInline, ProductVariantsInline, ProductLangInline]
    form = ProductAdminForm


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status', 'is_approved', 'created', 'updated')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['-created']
    search_fields = ['user', 'content', 'subject']


class ColorResource(resources.ModelResource):
    class Meta:
        model = Color
        fields = ('name', 'code',)


class ColorAdmin(ImportExportActionModelAdmin):
    resources_class = ColorResource
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']


class ProductLangugaeAdmin(admin.ModelAdmin):
    list_display = ['name', 'lang', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['lang']


class CategoryLangugaeAdmin(admin.ModelAdmin):
    list_display = ['name', 'lang', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['lang']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(ProductLang, ProductLangugaeAdmin)
admin.site.register(CategoryLang, CategoryLangugaeAdmin)
