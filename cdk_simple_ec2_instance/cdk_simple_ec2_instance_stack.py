from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)

class CdkSimpleUbuntuInstanceAsg(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a simple vpc
        vpc = ec2.Vpc(self, "MyVPC",
          max_azs=3
        )

        # Dynamically pull ubuntu ami id - needs environment var set CDK_DEFAULT_REGION
        dynamic_ubuntu_ami = ec2.MachineImage.lookup(
            name="*ubuntu-bionic-18.04-amd64-server*",
            owners=["099720109477"]
        )

        # Single Ubuntu EC2 instance in Private Subnet in an ASG of 1:1
        asg = autoscaling.AutoScalingGroup(
            self,
            "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=dynamic_ubuntu_ami,
        )
        
        # Bastion host to access Ubuntu host
        host = ec2.BastionHostLinux(self, "BastionHost",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )
        host.allow_ssh_access_from(ec2.Peer.ipv4("0.0.0.0/32"))
