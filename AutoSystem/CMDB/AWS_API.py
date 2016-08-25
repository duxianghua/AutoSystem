import boto3
import os
from CMDB.models import area,ec2_instances

class aws_api:
    def __init__(self,area_id):
        self.area_obj = area.objects.filter(pk=area_id)
        os.environ["AWS_DEFAULT_REGION"]=self.area_obj[0].area_region
        os.environ["AWS_ACCESS_KEY_ID"]=self.area_obj[0].area_access_key
        os.environ["AWS_SECRET_ACCESS_KEY"]=self.area_obj[0].area_private_key
        ec2_instances.objects.filter(ec2_area=self.area_obj).delete()
    def get_aws_instances(self):
        StateList=['running','stopped']
        ec2=boto3.resource('ec2')
        data=ec2.instances.all()
        count=0
        for i in data:
            tags = i.tags[0]['Value']
            type = i.instance_type
            id = i.instance_id
            create_time = i.launch_time
            private_ip = i.private_ip_address
            public_ip = i.public_ip_address
            state = i.state['Name']
            if not public_ip:
                public_ip="null"
            if state in StateList:
                try:
                    obj = ec2_instances.objects.get(ec2_id=id)
                    obj.ec2_area=self.area_obj[0]
                    obj.ec2_tags=tags
                    obj.ec2_type=type
                    obj.ec2_id=id
                    obj.ec2_create_time=create_time
                    obj.ec2_private_ip=private_ip
                    obj.ec2_public_ip=public_ip
                    obj.ec2_state=state
                    obj.save()
                except ec2_instances.DoesNotExist:
                    ec2_instances.objects.create(
                                                ec2_area=self.area_obj[0],
                                                ec2_tags=tags,
                                                ec2_type=type,
                                                ec2_id=id,
                                                ec2_create_time=create_time,
                                                ec2_private_ip=private_ip,
                                                ec2_public_ip=public_ip,
                                                ec2_state=state
                                                )
                count=count+1
        return count