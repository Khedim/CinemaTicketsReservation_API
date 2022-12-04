from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.http import response

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import *

from .models import *

from .permissions import IsAuthorOrReadOnly

# Create your views here.

# method 1
def no_rest_no_model(requset):
    data = [
        {
            'id': 1,
            'name': 'osama',
            'mobile': 32185
        },
        {
            'id': 2,
            'name': 'patout',
            'mobile': 3415
        },
    ]
    return JsonResponse(data, safe=False)

# method 2
def no_rest_model(requset):
    data = Guest.objects.all()
    print(data)
    print(type(data))
    response = {
        'guest': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# method 3
@api_view(['GET', 'POST'])
def FBV_list(requset):
    if requset.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    elif requset.method == 'POST':
        serializer = GuestSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(requset, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if requset.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    if requset.method == 'PUT':
        serializer = GuestSerializer(guest, data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif requset.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# method 4
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class CBV_pk(APIView):

    def get_obj(self, pk):
        return get_object_or_404(Guest, pk=pk)

    def get(self, request, pk):
        guest = self.get_obj(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_obj(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_obj(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# method 5 => mixins
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all() # variable must be writen like this
    serializer_class = GuestSerializer # variable must be writen like this
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all() # variable must be writen like this
    serializer_class = GuestSerializer # variable must be writen like this
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)


# method 6 => generics
class generic_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]

    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

class generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# method 7 => viewsets  you must set a router in urls.py above
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # filter_backend = [filters.SearchFilter] #does not working 
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['GET'])
def find_movie(request):
    queryset = Movie.objects.filter(
        hall = request.data['hall'],
        # movie = request.data['movie'],
    )
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    return Response(status=status.HTTP_201_CREATED)


# post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    