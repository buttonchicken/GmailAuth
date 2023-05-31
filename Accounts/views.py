from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils import authorize
import base64
from datetime import datetime

class Authorize(APIView):
    def get(self,request):
        query = ""
        try:
            query+="from:"+self.request.query_params.get("From")
            query+=" "
        except:
            pass
        try:
            query+="after:"+self.request.query_params.get("After")
            query+=" "
        except:
            pass
        try:
            query+="before:"+self.request.query_params.get("Before")
            query+=" "
        except:
            pass
        query = query.strip()
        print(query)
        service = authorize()
        res = service.users().messages().list(userId='me', q=str(query)).execute()
        mails = []
        if 'messages' in res:
            for r in res['messages']:
                mail_obj = {}
                message = service.users().messages().get(userId='me', id=r['id'], format="full").execute() # fetch the message using API
                payld = message['payload']
                headers=payld["headers"]
                for i in headers:
                    if i["name"]=="Subject":
                        mail_obj["Subject"]=i["value"]
                    if i["name"]=="Date":
                        mail_obj["Datetime"]=i["value"]
                    if i["name"]=="From":
                        mail_obj["From"]=i["value"].split("<")[1].replace(">","")
                    if i["name"]=="To":
                        mail_obj["To"]=i["value"]
                        break
                for p in payld["parts"]:
                    if p["mimeType"] in ["text/plain"]:
                        data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                        mail_obj["Body"]=data
                mails.append(mail_obj)
        for mail in mails:
            dstime=mail_obj["Datetime"].split(",")[1].replace("-","+").split("+")[0].strip()
            dtime = datetime.strptime(dstime, '%d %b %Y %H:%M:%S')
            Mail.objects.get_or_create(From = mail["From"],To = mail["To"],Subject = mail["Subject"],Body = mail["Body"],Time_received=dtime)
        return Response({'Emails':mails},status=status.HTTP_200_OK)