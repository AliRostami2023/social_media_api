from rest_framework.pagination import PageNumberPagination


class PostPaginations(PageNumberPagination):
    page_size = 100


class CommentPaginations(PageNumberPagination):
    page_size = 25
   