import json
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from djangoshop import settings
from ecomapp.forms.search import SearchForm
from ecomapp.forms.review import ProductReviewForm
from ecomapp.models.shop import Category, Product, ProductReview, Variants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


def search(request):
    query = None
    products = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(Q(name__icontains=query))
            else:
                products = Product.objects.filter(Q(name__icontains=query), category_id=catid)
    context = {
        'form': form,
        'query': query,
        'products': products,
    }
    return render(request, 'index.html', context)


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)

        results = []
        for product in products:
            product_json = product.name +" > " + product.category.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def base_view(request):
    template = "index.html"
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY
    products = Product.objects.all()
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
    }
    return render(request, template, context)


def add_review(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = ProductReview()
            review.subject = review_form.cleaned_data['subject']
            review.content = review_form.cleaned_data['content']
            review.rating = review_form.cleaned_data['rating']
            product = Product.objects.get(id=id, available=True)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, _("Ваш відгук надіслано. Дякуємо за ваш інтерес."))
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def product_view(request, id, slug):
    template = "shop/product_detail.html"

    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    products = Product.objects.all()

    if defaultlang != currentlang:
        try:
            prolang = Product.objects.raw(
                'SELECT p.id,p.articul,p.warranty,p.image_url,p.image,p.price,p.old_price,p.stock,p.variant,l.name,l.slug,l.description,l.meta_keywords,l.meta_description'
                'FROM ecomapp_product as p '
                'INNER JOIN ecomapp_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.id=%s and l.lang=%s', [id, currentlang])
            product = prolang[0]
        except:
            pass
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end
    images = product.images.all()

    product_reviews = ProductReview.approved.filter(product_id=id).order_by('-created')
    product_reviews_count = ProductReview.approved.count()
    review_form = ProductReviewForm()

    paginator = Paginator(product_reviews, 3)
    page = request.GET.get('page')
    try:
        product_reviews = paginator.page(page)
    except PageNotAnInteger:
        product_reviews = paginator.page(1)
    except EmptyPage:
        product_reviews = paginator.page(paginator.num_pages)

    context = {
        'product': product,
        'products': products,
        'images': images,
        'product_reviews': product_reviews,
        'product_reviews_count': product_reviews_count,
        'review_form': review_form,
    }
    if product.variant != "None":
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({
            'sizes': sizes, 'colors': colors,
            'variant': variant, 'query': query
        })
    return render(request, template, context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('shop/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def category_view(request, category_slug):
    template = "shop/product_list_by_category.html"

    category = get_object_or_404(Category, slug=category_slug)
    products_of_category = Product.objects.filter(category=category)

    paginator = Paginator(products_of_category, 8)
    page = request.GET.get('page')
    try:
        products_of_category = paginator.page(page)
    except PageNotAnInteger:
        products_of_category = paginator.page(1)
    except EmptyPage:
        products_of_category = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'products_of_category': products_of_category,
    }
    return render(request, template, context)
