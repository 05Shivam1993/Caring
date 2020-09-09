from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

# Create your views here.
@method_decorator(csrf_exempt,name='dispatch')
class UploadFile(APIView):
    # permission_classes = [TokenHasReadWriteScope]
    def post(self,request):
        try:
            dataset_name = request.data['dataset_name']
            dataset_description = request.data['dataset_description']
            modality = request.data['modality']
            file = request.data['file']
            project_name = request.data['project_name']
            project_description = request.data['project_description']

            payload1 = {
            'dataset_name':dataset_name,
            'dataset_description': dataset_description,
            'modality':modality
            }
            headers={'Authorization': 'Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbGlkIjoic2hpdmFtc3JpdmFzdGF2YTY1NkBnbWFpbC5jb20iLCJ1c2VyaWQiOjY2LCJleHAiOjE1OTk2ODA0NDd9.psY0b_PCAmOvotm9o38S_9jpfM_-9woYpo0lDMx2Ilg'}

            resp1 = requests.post('https://demo.carpl.ai/api/v1/create_dataset',headers=headers,data=payload1)
            dataset_id = resp1.json()['dataset_id']
            # print('dataset_id',dataset_id)

            payload2 = {
            'project_name':project_name,
            'project_description':project_description,
            'algorithm':14,
            'dataset_id':dataset_id,
            'findings':["finding1","finding2"]
            }
            # print(payload2)
            resp2 = requests.post('https://demo.carpl.ai/api/v1/create_inference_project',headers=headers,data=payload2)
            # print('Response',resp2.json())

            payload3 = {
                'dataset_id': dataset_id,
                'anon': '0'}

            #Change your path to that location where the file is present
            files = [('file', open('C:\\Users\\user\\Desktop\\caring\\'+file,'rb'))]

            resp3 = requests.post('https://demo.carpl.ai/api/v1/upload',headers=headers,data=payload3,files=files)

            return Response({"message":"File Uploaded Successfully"},status=200)
        except Exception as e:
            return Response({"message":"There is some error while uploading file"},status=400)
