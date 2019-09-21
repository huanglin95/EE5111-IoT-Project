
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json
from datetime import datetime
from datetime import timedelta

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient2"

# The unique hostname that &IoT; generated for
# this device.
HOST_NAME = "a3bf3bd3vxuu0i-ats.iot.ap-southeast-1.amazonaws.com"

# The relative path to the correct root CA file for &IoT;,
# which you have already saved onto this device.
ROOT_CA = "AmazonRootCA1(2).pem.txt"

# The relative path to your private key file that
# &IoT; generated for this device, which you
# have already saved onto this device.
PRIVATE_KEY = "217af20c79-private.pem.key"

# The relative path to your certificate file that
# &IoT; generated for this device, which you
# have already saved onto this device.
CERT_FILE = "217af20c79-certificate.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "Thing2_A0206810R"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)
  
# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)


# read and publish data from trainFD001.txt to your thing under AWS IoT platform
# To stop running this script, press Ctrl+C.

# Data Labels
sensor_name = ['s'+ str(i) for i in range(1,22)]
Data_Labels = ['id', 'timestamp', 'Matric_Number', 'te', 'os1', 'os2', 'os3'] + sensor_name

FD002_data = open("train_FD002.txt")
for row in FD002_data:
    # tranfer string to list format
    DataList = row.split()
    
    # get UTC time
    # e.g. UTC 2019-01-28 14:41:15.237
    timestamp = time.time()
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time+timedelta(hours=8)
    UTC = 'UTC '+ str(local_time)
    
    # martic number
    MatricNumber = 'A0206810R'
    
    # get the new data
    NewData = []
    # Overwrite column 'id' of the engine as 'FD001' + id
    NewData.append('FD002_' + DataList[0])
    # add one more columns 'timestamp' as timestamp in UTC
    NewData.append(UTC)
    # add one more column that contains the Matric number
    NewData.append(MatricNumber)
    for j in range(1,len(DataList)):
        NewData.append(DataList[j])
    
    # get label:data_value format
    Labels_Data={}
    for i in range(0,len(Data_Labels)):
        Labels_Data.update({Data_Labels[i]: NewData[i]})
    
    # get payload for updating data on AWS IoT platform
    payload={'state':{'reported':Labels_Data}}
    
    # transfer payload to json ducument
    payload_json=json.dumps(payload)

    # updata data on the AWS IoT platform
    myDeviceShadow.shadowUpdate(payload_json, myShadowUpdateCallback, 5)
    
    time.sleep(10)
