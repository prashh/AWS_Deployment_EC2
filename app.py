import time

from botocore.exceptions import ClientError

from creds import Creds
import boto3
import requests


creds = Creds("credentials.csv")

GIT_URL = "https://github.com/prashh/static_website"

REGION = "us-west-2"
SECURITY_GROUP = "sg-0e66bd644483bd39c"
IAM_PROFILE = "test-python"

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=creds.access_key_id,
    aws_secret_access_key=creds.secret_key,
    region_name=REGION
)


def provision_server():
    # Ubuntu Server 18.04 ID from the AWS panel
    image_id = "ami-003634241a8fcdec0"

    # Second smallest instance, free tier eligible.
    instance_type = "t2.micro"

    # Make this a command-line argument in the future.
    keypair_name = "test-python-deploy"

    response = {}
    try:
        response = ec2.run_instances(ImageId=image_id,
                                     InstanceType=instance_type,
                                     KeyName=keypair_name,
                                     SecurityGroupIds=[SECURITY_GROUP],
                                     IamInstanceProfile={'Name': IAM_PROFILE},
                                     MinCount=1,
                                     MaxCount=1)

        print("Provisioning instance...")
        # wait for server to be provisioned before returning anything
        time.sleep(30)
        return str(response['Instances'][0]['InstanceId'])

    except ClientError as e:
            print(e)


def get_instance(instanceId):
    instances = ec2.describe_instances(InstanceIds = [instanceId])
    instances = instances['Reservations'][0]['Instances']
    for instance in instances:
        return instance


def send_command_aws(commands=["echo hello"], instance="i-06cca6072e593a0ac"):
    ssm_client = boto3.client('ssm',
                              aws_access_key_id=creds.access_key_id,
                              aws_secret_access_key=creds.secret_key,
                              region_name=REGION)
    response = {}

    # time delay until command executes
    while True:
        try:
            response = ssm_client.send_command(
                InstanceIds=[instance],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': commands}, )
            break
        except ClientError as e:
            print("You may have an error in your command, or the machine is not up yet. ")
            time.sleep(10)

    command_id = response['Command']['CommandId']

    time.sleep(5)

    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance,
    )


def generate_git_commands(git_url=GIT_URL, start_command="sudo python3 hellopython/app.py", pip3_packages=[], additional_commands=[]):
    commands = []
    if ".git" in git_url:
        git_url = git_url[:-4]

    repo_name = git_url[git_url.rfind('/'):]

    # install dependencies
    commands.append("sudo apt-get update")
    commands.append("sudo apt-get install -y git")
    commands.append("sudo apt-get install -y python3")
    commands.append("sudo apt-get install -y python3-pip")

    commands.append("sudo rm -R hellopython")

    commands.append("pip3 --version")

    commands.append("sudo git clone " + git_url)
    # commands.append("cd " + repo_name)

    # install python dependencies
    for dependency in pip3_packages:
        commands.append("sudo pip3 install " + dependency)

    # run any additional custom commands
    for command in additional_commands:
        commands.append(command)

    # start program execution
    commands.append(start_command)

    return commands


# response = ec2.describe_instances()
# print(response)

# send_command()

# print(get_instance_ids())
new_instance=provision_server()

print("Waiting for instance to get in  running state....")

while True:
    state = get_instance(new_instance)['State']['Code']
    if 16 == state:
        break
    time.sleep(60)

print("Giving some more time for SSM....")

time.sleep(180)

print("Deploying the Web App...")
send_command_aws(commands=generate_git_commands(GIT_URL, pip3_packages=["flask"]), instance=new_instance)
time.sleep(60)

URL = get_instance(new_instance)["PublicDnsName"]
print('http://' + URL + ':5000')
print("Testing...")
r = requests.get('http://' + URL + ':5000')
if r.status_code != 200:
    raise Exception("Status Code not 200")
if r.text != "Hello World":
    raise Exception("Text does not match")

print("Deployment Succeeded.")
