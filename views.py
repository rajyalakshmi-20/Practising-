from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
from .leaveManagement import add_leave_with_calculation
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import *
import json
from .holiday_management import add_holidayy
from .password_reset_file import reset_password
from .add_employee_view import add_employee
from .utils import *


# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        username = serializer.validated_data['username']
        userId = User.objects.get(username = username).id
        return JsonResponse({
            "message":"User registered successfully",
            "data":user_data,
            "id":userId
        },
        status=  status.HTTP_201_CREATED
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        userId = User.objects.get(username = username).id
        return JsonResponse({
            "message":"User logged in successfully",
            "id":userId,
            "data":serializer.data,
        },
        status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def send_otp(request):
    email = (json.loads(request.body))['email']
    from .send_otp_logic import sendOtp
    resp = sendOtp(email)
    return JsonResponse({"message": "OTP sent successfully", 
                         "status":resp.status_code}, 
                        status=status.HTTP_200_OK)

@api_view(['POST'])
def confirm_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    cached_otp = cache.get(email)
    if cached_otp is None or cached_otp != otp:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    result = reset_password(email, password, confirm_password)  
    return result 

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_employee_view(request):
    if request.method == 'POST' and request.user.isAdmin == True:
        body = json.loads(request.body)
        resp = add_employee(body)
        return resp
    else:
        return JsonResponse({
            "status": "failed",
            "message": "User not authorized"
        },
        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def getAllEmployees(request):
    user_fields = User.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).order_by('id').values(
    'id',
    'username',
    'full_name',
    'emplyeeIdentficationCode',
    'joining_date',
    'phone',
    'department',
    'designation'
)

    user_data = [
        {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'emplyeeIdentficationCode': user['emplyeeIdentficationCode'],
            'joining_date': user['joining_date'],
            'phone': user['phone'],
            'department': user['department'],
            'designation': user['designation']
        }
        for user in user_fields
    ]

    return JsonResponse({'data': user_data})

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user(request):
    try:
        if request.user.isAdmin == False:
            raise Exception("user not authorised")
        
        else:
            data = json.loads(request.body)
            if data['email']:
                user = User.objects.get(email = data['email'])
                userId = user.id
                email = data['email']
                username = data['username']
                password = data['password']
                confirmPassword = data['confirmPassword']
                first_name = data['first_name']
                last_name = data['last_name']
                empId = data['emplyeeIdentficationCode']
                joining_date =  data['joining_date']
                phone = data['phone']
                department = data['department']
                designation = data['designation']

                if password != "" and password == confirmPassword:
                    user.set_password(password)
                    user.save()

                User.objects.filter(id = userId).update(
                    email=email,
                    username = username if username else "",
                    first_name=first_name if first_name else "",
                    last_name=last_name if last_name else "",
                    emplyeeIdentficationCode=empId if empId else "",
                    joining_date=joining_date if joining_date else "",
                    phone=phone if phone else "",
                    department=department if department else "",
                    designation=designation if designation else ""
                )

            return JsonResponse({
                "message":"User updated successfully"
            },
            status = status.HTTP_200_OK)


    except Exception as ex:
        return JsonResponse({
            "message":str(ex)
        },
        status = status.HTTP_401_UNAUTHORIZED)

    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def deactivate_user(request):
    try:
        if request.user.isAdmin == False:
            raise Exception("user not authorised")
        
        data = json.loads(request.body)
        user = User.objects.get(email=data['email'])
        user.is_active = False
        user.save()
        return JsonResponse({
            "message": f"User {user.username} with employee ID - {user.emplyeeIdentficationCode} deactivated from the employee list successfully",
            "status":"success"
        },
        status = status.HTTP_200_OK)

        
    except Exception as ex:
        return JsonResponse({
            "message": str(ex),
            "status":"failed"
        },
        status = status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_detail_view(request):
    try:
        userData = json.loads(request.body)
        fname = userData.get("first_name", "").strip()
        
        if not fname:
            return JsonResponse({
                "status": "Failed",
                "data": "No Data Passed"
            }, status=status.HTTP_400_BAD_REQUEST)

        min_similarity = 0.4  # Adjust the similarity threshold as needed
        matching_users = []

        users = User.objects.all()
        for user in users:
            similarity = sum(a == b for a, b in zip(fname, user.first_name)) / max(len(fname), len(user.first_name))
            if similarity >= min_similarity:
                userDetails = {
                    "email": user.email,
                    "first_Name": user.first_name,
                    "last_Name": user.last_name,
                    "empId": user.emplyeeIdentficationCode,
                    "joiningDate": user.joining_date,
                    "designation": user.designation,
                }
                matching_users.append(userDetails)

        if not matching_users:
            return JsonResponse({
                "status": "Failed",
                "data": "No matching data found"
            }, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            "status": "Success",
            "data": matching_users
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "data": "Query error: " + str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['POST'])
# def user_detail_view(request):
#     userData = json.loads(request.body)
#     fname = userData["first_Name"]
#     empId = userData["empId"]
#     des = userData["des"]
    
#     try:
#         if empId=='' and fname == "" and des == "":
#             return JsonResponse({
#                 "status": "Failed",
#                 "data": "No Data Passed"
#             },
#             status = status.HTTP_400_BAD_REQUEST)
#         elif empId and fname == "" and des == "":
#             user = User.objects.get(emplyeeIdentficationCode = empId)

#             userDetails = {
#                 "email":user.email,
#                 "first_Name":user.first_name,
#                 "last_Name":user.last_name,
#                 "empId":user.emplyeeIdentficationCode,
#                 "joiningDate":user.joining_date,
#                 }
            
#             return JsonResponse({
#                 "status":"Success",
#                 "data" :userDetails
#             },
#             status = status.HTTP_200_OK)
            
#         elif fname and empId == "" and des == "":
#             firstNames = []
#             users = User.objects.all()
#             for i in users:
#                 firstNames.append(i.first_name)

#             min_similarity = 0.1
#             matching_names = []

#             for name in firstNames:
#                 similarity = sum(a == b for a, b in zip(fname, name)) / max(len(fname), len(name))
#                 if similarity >= min_similarity:
#                     matching_names.append(name)

#             queryedUsers = []
#             for name in matching_names:
#                 user = User.objects.get(first_name = name)
#                 userDetails = {
#                 "email":user.email,
#                 "first_Name":user.first_name,
#                 "last_Name":user.last_name,
#                 "empId":user.emplyeeIdentficationCode,
#                 "joiningDate":user.joining_date,
#                 }
#                 queryedUsers.append(userDetails)

#             if queryedUsers == []:
#                 return JsonResponse({
#                 "status": "Failed",
#                 "data": "Data not found"
#             },
#             status = status.HTTP_404_NOT_FOUND)

#             return JsonResponse({
#                 "status":"Success",
#                 "data" :queryedUsers
#             },
#             status = status.HTTP_200_OK)

#         elif des and empId == "" and fname == "":
#             users = User.objects.filter(designation=des)
#             if not users:
#                 return JsonResponse({
#                 "status": "Failed",
#                 "data": "Inavalid input"
#             },
#             status = status.HTTP_400_BAD_REQUEST)
#             queryedUsers = []
#             for user in users:
#                 userDetails = {
#                     "email": user.email,
#                     "first_Name": user.first_name,
#                     "last_Name": user.last_name,
#                     "empId": user.emplyeeIdentficationCode,
#                     "joiningDate": user.joining_date,
#                     "designation": user.designation,
#                 }
#                 queryedUsers.append(userDetails)

#             return JsonResponse({
#                 "status": "Success",
#                 "data": queryedUsers
#             },
#             status = status.HTTP_200_OK)
        
#     except Exception:
#         return JsonResponse({
#                 "status": "Failed",
#                 "data": "Query not Found"
#             },
#             status = status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_leave(request):
    user = request.user
    data = request.data

    leave_type = data.get('leave_type')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    return add_leave_with_calculation(user, leave_type, start_date_str, end_date_str)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leave_history(request):
    user = request.user
    leave_history = Leave.objects.filter(user=user)
    leave_data = [
        {
            'leave_type': leave.leave_type,
            'start_date': leave.start_date,
            'end_date': leave.end_date
        }
        for leave in leave_history
    ]
    return Response(leave_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_holiday(request):
    if request.method == 'POST' and request.user.isAdmin == True:  # Note the change from request.isAdmin to request.user.isAdmin
        data = json.loads(request.body)
        date_str = data['date']
        name = data['name']

        if not date_str:
            return JsonResponse({"message": "Date is required"}, status=400)
        
        # Call the add_holiday function from holiday_management.py
        result, status_code = add_holidayy(date_str, name)

        return JsonResponse(result, status=status_code)
    
    return JsonResponse({"message": "Method not allowed"}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_holidays(request):
    holidays = Holiday.objects.all()
    holidays_list = [{"date": holiday.date.strftime('%Y-%m-%d'), "name": holiday.name} for holiday in holidays]
    return JsonResponse({"holidays": holidays_list})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def punch_in_view(request):
    user = request.user
    current_time, current_date = get_current_time_and_date()

    # check already punched
    try:
        attendance_record = Attendance.objects.get(user=user, date=current_date)
        punch_times = attendance_record.punch_times

        if len(punch_times) % 2 != 0:
            return JsonResponse({"message": "You must punch out before punching in again"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(punch_times) >= 24:
            return JsonResponse({"message": "Limit Exceded. You have already punched in and out 12 times today"}, status=status.HTTP_400_BAD_REQUEST)

        punch_times.append(current_time.strftime('%H:%M:%S'))
        attendance_record.punch_times = punch_times
        attendance_record.save()
    except Attendance.DoesNotExist:
        # First Punch In
        attendance_record = Attendance.objects.create(user=user, date=current_date, punch_times=[current_time.strftime('%H:%M:%S')])

    return JsonResponse({
        "message": "Punch-in recorded successfully",
        "punch_in_time": current_time.strftime('%H:%M:%S'),
        "is_holiday": attendance_record.is_holiday
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def punch_out_view(request):
    user = request.user
    current_time, current_date = get_current_time_and_date()

    try:
        attendance_record = Attendance.objects.get(user=user, date=current_date)
        punch_times = attendance_record.punch_times

        if len(punch_times) % 2 != 1:
            return JsonResponse({"message": "You must punch in before punching out"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(punch_times) >= 24:
            return JsonResponse({"message": "Limit Exceeded. You have already punched in and out 12 times today"}, status=status.HTTP_400_BAD_REQUEST)
        
        punch_times.append(current_time.strftime('%H:%M:%S'))
        attendance_record.punch_times = punch_times

        # Total Punch time
        total_punch_time = timezone.timedelta()
        for i in range(0, len(punch_times), 2):
            punch_in_time = datetime.strptime(punch_times[i], '%H:%M:%S')
            punch_out_time = datetime.strptime(punch_times[i + 1], '%H:%M:%S')
            punch_duration = punch_out_time - punch_in_time
            total_punch_time += punch_duration

        attendance_record.total_punch_time = total_punch_time
        attendance_record.save()

        return JsonResponse({
            "message": "Punch-out recorded successfully",
            "punch_out_time": current_time.strftime('%H:%M:%S'),
            "total_punch_time": str(total_punch_time)
        }, status=status.HTTP_201_CREATED)

    except Attendance.DoesNotExist:
        return JsonResponse({
            "message": "No corresponding attendance record found"
        }, status=status.HTTP_400_BAD_REQUEST)