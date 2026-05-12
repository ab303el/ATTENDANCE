from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required , user_passes_test
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

from datetime import time
from django.utils import timezone
from rest_framework.permissions import IsAdminUser      #only managers/admins

from django.contrib import messages #to show alerts login and account creation success

from django.core.exceptions import PermissionDenied     #admin only

from .forms import EmployeeSignupForm # Import your new form

from django.contrib.auth.models import Group

class ManagerLateDashboardAPI(generics.ListCreateAPIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1. Get today's date as a string (avoids the fromisoformat error)
        today_str = timezone.now().date().isoformat() 
        
        # 2. Get all records for today from the DB
        today_records = Attendance.objects.filter(date=today_str)

        # 3. Filter in Python to find late employees (Clock in > 9:00 AM)
        work_start_time = time(9, 0, 0) 
        late_records = []
        
        for record in today_records:
            # Ensure clock_in exists, then compare only the time portion
            if record.clock_in and record.clock_in.time() > work_start_time:
                late_records.append(record)

        # 4. Serialize and Return
        serializer = AttendanceSerializer(late_records, many=True)
        
        return Response({
            "status": "success",
            "manager_user": request.user.username,
            "date": today_str,
            "late_count": len(late_records),
            "late_employees": serializer.data
        })



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


# web page views
#signup view

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the router which decides the dashboard
            return redirect('dashboard-router')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # AUTO-CREATE GROUP IF MISSING
            employee_group, created = Group.objects.get_or_create(name='Employee')
            user.groups.add(employee_group)
            
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard-router')
    else:
        form = EmployeeSignupForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def dashboard_router(request):
    """
    Decides where to send the user safely.
    """
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin-dashboard')
    
    # Check for group safely without crashing
    if request.user.groups.filter(name='Employee').exists():
        return redirect('employee-dashboard')
        
    # Default fallback so no one gets 'bounced'
    return redirect('employee-dashboard')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('employee_dashboard')
    
    # Fetch EVERY attendance record for the admin to see
    attendances = Attendance.objects.all().order_by('-date', '-clock_in')
    
    return render(request, 'core/dashboard.html', {'attendances': attendances})

@login_required
def employee_dashboard(request):
    # 1. Get the employee profile for the logged-in user
    try:
        employee_profile = Employee.objects.get(user=request.user)
        # 2. Get only THEIR attendance records
        attendances = Attendance.objects.filter(employee=employee_profile).order_by('-date')
    except Employee.DoesNotExist:
        attendances = []

    return render(request, 'core/employee_dashboard.html', {'attendances': attendances})

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

@login_required
def attendance_action(request):
    if request.method == 'POST':
        try:
            employee_profile = Employee.objects.get(user=request.user)
            
            # Create the attendance record
            Attendance.objects.create(
                employee=employee_profile,
                date=timezone.now().date(),
                clock_in=timezone.now()
            )
            messages.success(request, "Clocked in successfully!")
        except Employee.DoesNotExist:
            messages.error(request, "Employee profile not found.")
            
    return redirect('dashboard-router')
