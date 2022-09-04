from information.serializers import InformationSerializer
from accounts.models import Users
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_editors(request):
    if request.method == "GET":
        try:
            # Users table에서 editor 정보만 선택한다.
            editors = Users.objects.filter(role=True)

            # list를 반환하기 위해 many=True 조건을 단다.
            serialized_editors = InformationSerializer(editors, many=True)
            # return Response({"code": 200, "editors": serialized_editors.data})
            return render(request, 'test.html', {'info': serialized_editors.data})
        except:
            return Response({"code": 404, "message": "Cannot find categories"})
    else:
        return Response({"code": 400, "message": "Invalid method"})
