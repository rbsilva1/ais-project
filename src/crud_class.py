import os
import boto3
from dotenv import load_dotenv

load_dotenv()


class EC2Manager:
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.ec2 = boto3.resource(
            "ec2",
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def create_instance(self, image_id=None):
        image_id = image_id or os.getenv("AWS_AMI_ID")
        instances = self.ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName=os.getenv("AWS_KEY_PAIR"),
            SecurityGroupIds=[os.getenv("AWS_SG_ID")],
            SubnetId=os.getenv("AWS_SUBNET_ID"),
        )

        instance_id = instances[0].id
        print(f"[INSTÂNCIA CRIADA]: {instance_id}")

    def list_instances(self):
        result = []
        for instance in self.ec2.instances.all():
            info = {
                "id": instance.id,
                "state": instance.state["Name"],
                "type": instance.instance_type,
                "public_ip": instance.public_ip_address,
            }
            result.append(info)
        return result

    def get_instance(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        return {
            "id": instance.id,
            "state": instance.state["Name"],
            "type": instance.instance_type,
            "public_ip": instance.public_ip_address,
        }

    def start_instance(self, instance_id):
        self.ec2.Instance(instance_id).start()
        print(f"[INSTÂNCIA INICIADA] {instance_id}")

    def stop_instance(self, instance_id):
        self.ec2.Instance(instance_id).stop()
        print(f"[INSTÂNCIA PAUSADA] {instance_id}")

    def change_instance_type(self, instance_id, new_type):
        instance = self.ec2.Instance(instance_id)
        instance.stop()
        instance.wait_until_stopped()
        instance.modify_attribute(InstanceType={"Value": new_type})
        instance.start()
        print(f"[ATUALIZOU] {instance_id} [PARA] {new_type}")
        self.ec2.Instance(instance_id).terminate()
        print(f"[INSTÂNCIA ENCERRADA] {instance_id}")
