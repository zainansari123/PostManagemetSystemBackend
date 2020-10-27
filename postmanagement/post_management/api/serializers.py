from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from rest_framework.serializers import *
from ..models import *
# from admin_panel.models import *
from rest_framework.exceptions import APIException
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
import random
from datetime import date, datetime

# import logging
# accounts_serializer = logging.getLogger('accounts')


class TaskSerializer(ModelSerializer):
    class Meta:
        model = TaskWork
        fields='__all__'


class EntryUpdateSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.source = validated_data.get('source', instance.source)
        instance.post_type = validated_data.get('post_type', instance.post_type)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.task_status = validated_data.get('task_status', instance.task_status)
        instance.save()
        return instance

    class Meta:
        model = TaskWork
        fields = '__all__'


class CreateTaskSerializer(Serializer):
    task_id = CharField(error_messages={"required": "task_id key is required", "blank": "task_id is required"})
    assigned_to = CharField(error_messages={"required": "assigned_to key is required", "blank": "assigned_to is required"})
    customer_name = CharField(error_messages={"required": "customer_name key is required", "blank": "customer_name is required"})
    customer_mobile = CharField(error_messages={"required": "customer_mobile key is required", "blank": "customer_mobile is required"})
    customer_address = CharField(error_messages={"required": "customer_address key is required", "blank": "customer_address is required"})
    post_type = CharField(error_messages={"required": "post_type key is required", "blank": "post_type is required"})
    priority = CharField(error_messages={"required": "priority key is required", "blank": "priority is required"})
    remarks = CharField(error_messages={"required": "remarks key is required", "blank": "remarks is required"})
    task_status = CharField(error_messages={"required": "task_status key is required", "blank": "task_status is required"})

    def validate(self, data):
        task_id=data['task_id']
        assigned_to=data['assigned_to']
        # if not isinstance(assigned_to, int):
        #     raise ValidationError('Please enter user id')
        if task_id:
            qs = TaskWork.objects.filter(id=task_id)
            if qs.exists():
                raise ValidationError("Task id Already Exists")
        return data

    def create(self, validated_data):
        customer_name=validated_data['customer_name']
        customer_obj=''
        qs = Customer.objects.filter(name=customer_name)
        if qs.exists():
            print(qs)
            customer_obj=qs.first()
            customer_obj.mobile=validated_data['customer_mobile']
            customer_obj.address=validated_data['customer_address']
            customer_obj.save()
        if not qs.exists():
            print('-------------------------------')
            customer_obj=Customer(name=validated_data['customer_name'],mobile=validated_data['customer_mobile'],address=validated_data['customer_address'])
            customer_obj.save()

        task = TaskWork(id=validated_data['task_id'],assigned_to_id=validated_data['assigned_to'],source=customer_obj.id,
                    post_type=validated_data['post_type'],priority=validated_data['priority'],
                    remarks=validated_data['remarks'],task_status=validated_data['task_status'])
        task.save()
        return validated_data
