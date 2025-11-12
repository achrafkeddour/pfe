# remplir mongodb user (docker-compose version)

```
use free5gc 

docker exec -it mongodb mongo
```

```
// 1. Authentication data
db.getCollection("subscriptionData.authenticationData.authenticationSubscription").insertOne({
  "ueId": "imsi-208930000000001",
  "authenticationMethod": "5G_AKA",
  "encPermanentKey": "8baf473f2f8fd09487cccbd7097c6862",
  "authenticationManagementField": "8000",
  "algorithmId": "milenage",
  "encOpcKey": "8e27b6af0e692e750f32667a3b14605d",
  "sequenceNumber": "000000000023"
})

// 2. Access and Mobility data
db.getCollection("subscriptionData.provisionedData.amData").insertOne({
  "ueId": "imsi-208930000000001",
  "servingPlmnId": "20893",
  "subscribedUeAmbr": {
    "uplink": "1 Gbps",
    "downlink": "2 Gbps"
  },
  "nssai": {
    "defaultSingleNssais": [
      {"sst": 1, "sd": "010203"},
      {"sst": 1, "sd": "112233"}
    ],
    "singleNssais": []
  },
  "gpsis": ["msisdn-208930000000001"]
})

// 3. Session Management data for slice 1
db.getCollection("subscriptionData.provisionedData.smData").insertOne({
  "ueId": "imsi-208930000000001",
  "servingPlmnId": "20893",
  "singleNssai": {"sst": 1, "sd": "010203"},
  "dnnConfigurations": {
    "internet": {
      "pduSessionTypes": {"defaultSessionType": "IPV4", "allowedSessionTypes": ["IPV4"]},
      "sscModes": {"defaultSscMode": "SSC_MODE_1", "allowedSscModes": ["SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"]},
      "5gQosProfile": {
        "5qi": 9,
        "arp": {"priorityLevel": 8, "preemptCap": "", "preemptVuln": ""},
        "priorityLevel": 8
      },
      "sessionAmbr": {"uplink": "1000 Mbps", "downlink": "1000 Mbps"},
      "staticIpAddress": []
    }
  }
})

// 4. Session Management data for slice 2
db.getCollection("subscriptionData.provisionedData.smData").insertOne({
  "ueId": "imsi-208930000000001",
  "servingPlmnId": "20893",
  "singleNssai": {"sst": 1, "sd": "112233"},
  "dnnConfigurations": {
    "internet": {
      "pduSessionTypes": {"defaultSessionType": "IPV4", "allowedSessionTypes": ["IPV4"]},
      "sscModes": {"defaultSscMode": "SSC_MODE_1", "allowedSscModes": ["SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"]},
      "5gQosProfile": {
        "5qi": 8,
        "arp": {"priorityLevel": 8, "preemptCap": "", "preemptVuln": ""},
        "priorityLevel": 8
      },
      "sessionAmbr": {"uplink": "1000 Mbps", "downlink": "1000 Mbps"},
      "staticIpAddress": []
    }
  }
})

// 5. SMF Selection data
db.getCollection("subscriptionData.provisionedData.smfSelectionSubscriptionData").insertOne({
  "ueId": "imsi-208930000000001",
  "servingPlmnId": "20893",
  "subscribedSnssaiInfos": {
    "01010203": {"dnnInfos": [{"dnn": "internet"}]},
    "01112233": {"dnnInfos": [{"dnn": "internet"}]}
  }
})
```



## execute 
```
docker exec -it ueransim ./nr-ue -c ./config/uecfg.yaml
```

## check
```
# Check the network interfaces
ip addr show uesimtun0
ip addr show uesimtun1

# Test connectivity through each interface
ping -I uesimtun0 -c 4 8.8.8.8
ping -I uesimtun1 -c 4 8.8.8.8

# Test DNS resolution and web access
ping -I uesimtun0 -c 4 google.com

# You can also test with curl
curl --interface uesimtun0 http://www.google.com
```
