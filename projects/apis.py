
from rest_framework import generics, response, status, serializers
import requests
from django.db import connection


class ProjectApi(generics.GenericAPIView):
    """
    api to return list of projects in circumference
    """
    queryset = ""

    def get(self, request, *args, **kwargs):
        zipcode = self.request.query_params.get('zipcode', None)
        range = self.request.query_params.get('range', None)
        if zipcode is None or range is None:
            raise serializers.ValidationError("missing query param zipcode or range.")
        rating_system = self.request.query_params.get('rating_system', '')
        project_type = self.request.query_params.get('project_type', '')
        url = "http://api.zip-codes.com/ZipCodesAPI.svc/1.0/FindZipCodesInRadius?zipcode="+zipcode+"&minimumradius=0&maximumradius="+range+"&key=HH7CKSM3KF5K7FK8S8S2"
        proj = requests.get(url)
        zipcode = []
        if "DataList" in proj.json():
            for item in proj.json()["DataList"]:
                zipcode.append(str(item["Code"]))
        result = []
        cur = connection.cursor()
        cur.execute("select d.id, d.name, d.rating_system, c.credit_id, c.name as credit_name, c.points_awarded as credit_awarded, d.street, d.city, d.state, d.zip, d.country, d.email, d.date_registered, d.date_certified, d.gross_area, d.total_prop_area, d.certification_level, d.confidential, d.status, d.points_awarded, d.clean_owner_type, d.clean_space_type, c.rpc_awarded from project_details_clean as d join project_credits as c on d.id = c.project_id where c.credit_id='EAc1' and d.rating_system like '%NC%' and d.zip in "+str(tuple(zipcode))+" group by c.credit_id, d.id;")
        for obj in cur.fetchall():
            project = {}
            project["id"] = obj[0]
            project["name"] = obj[1]
            project["rating_system"] = obj[2]
            project["credit_id"] = obj[3]
            project["credit_name"] = obj[4]
            project["credit_awarded"] = obj[5]
            project["street"] = obj[6]
            project["city"] = obj[7]
            project["state"] = obj[8]
            project["zipcode"] = obj[9]
            project["country"] = obj[10]
            project["email"] = obj[11]
            project["date_registered"] = obj[12]
            project["date_certified"] = obj[13]
            project["gross_area"] = obj[14]
            project["total_prop_area"] = obj[15]
            project["certification_level"] = obj[16]
            project["confidential"] = obj[17]
            project["status"] = obj[18]
            project["points_awarded"] = obj[19]
            project["clean_owner_type"] = obj[20]
            project["clean_space_type"] = obj[21]
            project["rpc_awarded"] = obj[22]
            project["flag_attempted"] = False if project["status"] is "Unattempted" else True
            result.append(project)
        return response.Response(data=result, status=status.HTTP_200_OK)
