import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Category, Ad, Selection
from ads.permissions import SelectionUpdatePermissions
from ads.serializers import AdListSerializer, SelectionListSerializer, \
    SelectionDetailSerializer, SelectionSerializer, AdSerializer, CategoryCreateSerializer, AdCreateSerializer, \
    AdDetailSerializer
from avito import settings


def root(request):
    return JsonResponse({
        "status": "ok"
    })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):

        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


# @method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    # model = Category
    # fields = ["name"]
    #
    # def post(self, request, *args, **kwargs):
    #     category_data = json.loads(request.body)
    #
    #     category = Category.objects.create(
    #         name=category_data["name"],
    #     )
    #
    #     return JsonResponse({
    #         "id": category.id,
    #         "name": category.name,
    #     })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = 'cat/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        category = request.GET.get("cat", None)
        if category:
            self.queryset = self.queryset.filter(
                category__id__icontains=category
            )

        text = request.GET.get("text", None)
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text
            )

        ad_location = request.GET.get("location", None)
        if ad_location:
            self.queryset = self.queryset.filter(
                author__locations__name__icontains=request.GET.get("location")
            )

        price_from = request.GET.get("price_from", None)
        if price_from:
            self.queryset = self.queryset.filter(
                price__gt=price_from
            )

        price_to = request.GET.get("price_to", None)
        if price_to:
            self.queryset = self.queryset.filter(
                price__lt=price_to
            )
        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer


# @method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = AdCreateSerializer
    # model = Ad
    # fields = ["name", "price", "description", "is_published", "image", "author_id", "category_id"]
    #
    # def post(self, request, *args, **kwargs):
    #     ad_data = json.loads(request.body)
    #
    #     ad = Ad.objects.create(
    #         name=ad_data["name"],
    #         price=ad_data["price"],
    #         description=ad_data["description"],
    #         author_id=ad_data["author_id"],
    #         category_id=ad_data["category_id"],
    #         is_published=ad_data["is_published"],
    #         image=ad_data["image"]
    #     )
    #
    #     return JsonResponse({
    #         "id": ad.id,
    #         "name": ad.name,
    #         "author_id": ad.author_id,
    #         "price": ad.price,
    #         "description": ad.description,
    #         "category_id": ad.category_id,
    #         "is_published": ad.is_published,
    #     })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "price", "description", "is_published"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.is_published = ad_data["is_published"]
        self.object.author_id = ad_data["author_id"]
        self.object.category_id = ad_data["category_id"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "category_id": self.object.category_id,
            "is_published": self.object.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = 'ad/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "category_id": self.object.category_id,
            "is_published": self.object.is_published,
            "image": self.object.image.url
        })


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated]


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermissions]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermissions]