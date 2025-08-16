// create a file named 'subscribers.js'

db.subscribers.insertMany([
  {
    "imsi": "901700000000001",        // IMSI of UE 1
    "security": {
      "k": "465B5CE8B199B49FAA5F0A2EE238A6BC",   // UE key
      "opc": "E8ED289DEBA952E4283B54E88E6183CA", // Operator Code
      "amf": "8000"                              // Authentication Management Field
    },
    "slice": [
      {
        "sst": 1,    // Slice/Service Type
        "sd": "010203" // Slice Differentiator (can be "null" if not needed)
      }
    ],
    "msisdn": ["0001"],   // Optional phone number
    "schema_version": 1
  },
  {
    "imsi": "901700000000002",        // IMSI of UE 2
    "security": {
      "k": "465B5CE8B199B49FAA5F0A2EE238A6BD",
      "opc": "E8ED289DEBA952E4283B54E88E6183CB",
      "amf": "8000"
    },
    "slice": [
      {
        "sst": 1,
        "sd": "010203"
      }
    ],
    "msisdn": ["0002"],
    "schema_version": 1
  }
]);
