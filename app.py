#!/usr/bin/env python3

from aws_cdk import core
from aws_cdk.core import Environment
import os
from cdk_simple_ec2_instance.cdk_simple_ec2_instance_stack import CdkSimpleUbuntuInstanceAsg

AWS_ENV={
    'account': os.environ['CDK_DEFAULT_ACCOUNT'],
    'region': os.environ['CDK_DEFAULT_REGION']
}

app = core.App()
CdkSimpleUbuntuInstanceAsg(app, "cdk-simple-ubuntu-instance-asg", env=AWS_ENV)

app.synth()
