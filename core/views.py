from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  #the bouncer
from rest_framework.pagination import PageNumberPagination  # Import the paginator
from .models import Attendance, Employee
from .serializers import AttendanceSerializer, EmployeeSerializer
from rest_framework.views import APIView
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import generics   # Filtering, Searching, and Sorting.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter

# class AttendanceListCreateAPI(APIView):

#     # 1. Require a valid JWT Token for this entire view
#     permission_classes = [IsAuthenticated]

#     serializer_class = AttendanceSerializer
#     # 1. Require a valid JWT Token for this entire view
#     @extend_schema(responses=AttendanceSerializer(many=True), operation_id="list_attendance")
#     def get(self, request):
#         # 2. Object-Level Security (Filtering by the logged-in user)
#         # request.user is magically populated by the JWT token!
#         # We find the employee profile linked to the logged-in user.
#         employee_profile = Employee.objects.get(user = request.user)

#         # Only fetch records belonging to THIS employee.
#         records = Attendance.objects.filter(employee = employee_profile).order_by('-date')  # Order by newest first

#         # 1. Instantiate the paginator
#         paginator = PageNumberPagination()

#         # 2. Slice the database records based on the ?page= parameter in the URL
#         paginated_records = paginator.paginate_queryset(records , request)

#         # 3. Serialize ONLY the sliced records (e.g., just the 10 records for page 1)
#         serializer = AttendanceSerializer(paginated_records , many = True)

#         # 4. Return a special paginated response
#         return paginator.get_paginated_response(serializer.data)


#         # records = Attendance.objects.all()
#         # serializer = AttendanceSerializer(records, many=True)
#         # return Response(serializer.data)
    
#     @extend_schema(request=AttendanceSerializer, responses=AttendanceSerializer)
#     def post(self, request):
#         # 3. Secure Creation
#         # We don't trust the client to send "employee: 1" in the JSON body.
#         # Malicious users could fake it. Instead, we force the employee ID 
#         # based on the token making the request.
#         employee_profile = Employee.objects.get(user = request.user)


#         serializer = AttendanceSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save the record, forcefully attaching it to the logged-in employee
#             serializer.save(employee = employee_profile)
#             # serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceListCreateAPI(generics.ListCreateAPIView):
    
    #basic setup
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    #Enabling the filter engine
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]

    #Define the rules
    filterset_fields = ['date']                  #exact matches
    search_fields = ['employee__name']           #partial text search (spanning the relationship)
    ordering_fields = ['date' , 'clock_in']     #allowed sorting fields

    #secure the data (get)
    def get_queryset(self):
        """
        This automatically grabs the data, applies pagination, 
        AND applies any filters the user puts in the URL!
        """
        employee_profile = Employee.objects.get(user = self.request.user)
        
        return Attendance.objects.filter(employee = employee_profile)
    
    #secure the creation(post)
    def perform_create(self, serializer):
        """
        This intercepts the POST save to attach the logged-in user.
        """
        employee_profile = Employee.objects.get(user = self.request.user)
        serializer.save(employee = employee_profile)   


class EmployeeListCreateAPI(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = EmployeeSerializer

    @extend_schema(responses=EmployeeSerializer(many=True), operation_id="list_employees")
    def get(self, request):

        # employee_profile = Employee.objects.get(user = request.user)

        records = Employee.objects.filter(user = request.user).order_by('-id')

        paginator = PageNumberPagination()

        paginator_records = paginator.paginate_queryset(records , request)

        serializer = EmployeeSerializer(paginator_records, many=True)

        return paginator.get_paginated_response(serializer.data)

        # return Response(serializer.data)
    
    @extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AttendanceDetailAPI(APIView):

    permission_classes = [IsAuthenticated]


    serializer_class = AttendanceSerializer

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            raise Http404 # Changed from return to raise
        
    @extend_schema(operation_id="retrieve_attendance")
    def get(self, request, pk):
        attendance = self.get_object(pk=pk)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)
    
    @extend_schema(request=AttendanceSerializer, responses=AttendanceSerializer)
    def patch(self, request, pk):
        attendance = self.get_object(pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        attendance = self.get_object(pk)
        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        
class EmployeeDetailAPI(APIView):

    permission_classes = [IsAuthenticated]

    serializer_class = EmployeeSerializer

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404 # Changed from return to raise
        
    @extend_schema(operation_id="retrieve_employee")
    def get(self, request, pk):
        employee = self.get_object(pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
   
    @extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
    def patch(self, request, pk):
        employee = self.get_object(pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
