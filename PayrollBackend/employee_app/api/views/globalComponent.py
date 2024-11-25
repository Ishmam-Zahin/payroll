from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.db import transaction
from django.http import Http404

from user_app.api.permissions import IsAdminUser
from employee_app.models import GlobalComponent, GlobalComponentConditions
from employee_app.api.serializers import GlobalComponentSerializer, GlobalComponentConditionSerializer
from employee_app.api.permissions import AdminOrSafeMethod

class GlobalComponent_List(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get(self, request):
        objs = GlobalComponent.objects.all().prefetch_related('globalConditions')
        serializer = GlobalComponentSerializer(objs, many = True)

        return Response(serializer.data)
    
    def post(self, request):
        with transaction.atomic():
            componentData = request.data.pop('component', None)
            conditionsData = request.data.pop('conditions', None)

            if not componentData or not conditionsData:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid Format'})
            
            serializer = GlobalComponentSerializer(data = componentData)

            if serializer.is_valid():
                component = serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
            
            for data in conditionsData:
                data['global_component'] = component.id
            
            serializer2 = GlobalComponentConditionSerializer(data = conditionsData, many = True)

            if serializer2.is_valid():
                serializer2.save()
            else:
                transaction.set_rollback(True)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer2.errors)
            

            return Response({'message': 'successfull'})


class GlobalComponent_Detail(APIView):
    def getComponent(self, pk):
        try:
            return GlobalComponent.objects.get(id = pk)
        except:
            raise Http404
    
    def get(self, request, pk):
        component = self.getComponent(pk)
        serializer = GlobalComponentSerializer(component)

        return Response(serializer.data)
    
    def put(self, request, pk):
        with transaction.atomic():
            component = self.getComponent(pk)
            componentConditions = component.globalConditions.all()
            componentConditions = list(componentConditions)

            componentData = request.data.pop('component', None)
            conditionsData = request.data.pop('conditions', None)

            if not componentData or not conditionsData:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid Format'})
            
            serializer = GlobalComponentSerializer(component, data = componentData)
            if serializer.is_valid():
                serializer.save()
            else:
                transaction.set_rollback(True)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
            
            for data in conditionsData:
                if 'id' in data:
                    tmp = data.pop('id', None)
                    condition = None
                    for componentCondition in componentConditions:
                        if componentCondition.id == tmp:
                            condition = componentCondition
                            componentConditions.remove(componentCondition)
                            break
                    if condition is None:
                        transaction.set_rollback(True)
                        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'message': 'corrupted data'})
                    tmpSerializer = GlobalComponentConditionSerializer(condition, data = data)
                    if tmpSerializer.is_valid():
                        tmpSerializer.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=tmpSerializer.errors)
                else:
                    data['global_component'] = component.id
                    tmpSerializer = GlobalComponentConditionSerializer(data = data)
                    if tmpSerializer.is_valid():
                        tmpSerializer.save()
                    else:
                        transaction.set_rollback(True)
                        return Response(status=status.HTTP_400_BAD_REQUEST, data=tmpSerializer.errors)
            
            for condition in componentConditions:
                condition.delete()       

            return Response(status=status.HTTP_200_OK, data = {'message': 'ok'})
    
    def delete(self, request, pk):
        component = self.getComponent(pk)
        component.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})
