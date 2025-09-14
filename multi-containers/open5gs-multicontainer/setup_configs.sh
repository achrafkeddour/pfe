#!/bin/bash

# Créer le répertoire config
mkdir -p config

# Fonction pour créer les fichiers de configuration
create_config() {
    local component=$1
    local ip=$2
    
    cat > config/${component}.yaml << EOF
logger:
  file: /open5gs/install/var/log/open5gs/${component}.log
  level: info

global:
  max-pool: 10000
  packet-pool: 10000

${component}:
  sbi:
    server:
      - address: ${ip}
        port: 7777
    client:
EOF

    # Configuration spécifique pour chaque composant
    case ${component} in
        nrf)
            cat >> config/${component}.yaml << EOF
      nrf:
        - uri: http://10.45.0.10:7777
EOF
            ;;
        amf)
            cat >> config/${component}.yaml << EOF
      nrf:
        - uri: http://10.45.0.10:7777
      scp:
        - uri: http://10.45.0.10:7777
  ngap:
    server:
      - address: ${ip}
  metrics:
    server:
      - address: ${ip}
        port: 9090
  guami:
    - plmn_id:
        mcc: 001
        mnc: 01
      amf_id:
        region: 2
        set: 1
  tai:
    - plmn_id:
        mcc: 001
        mnc: 01
      tac: 1
  plmn_support:
    - plmn_id:
        mcc: 001
        mnc: 01
      s_nssai:
        - sst: 1
  security:
    integrity_order: [NIA2, NIA1, NIA0]
    ciphering_order: [NEA0, NEA1, NEA2]
  network_name:
    full: Open5GS
  amf_name: open5gs-amf0
EOF
            ;;
        smf)
            cat >> config/${component}.yaml << EOF
      nrf:
        - uri: http://10.45.0.10:7777
  pfcp:
    server:
      - address: ${ip}
    client:
      upf:
        - address: 10.45.0.13
  gtpc:
    server:
      - address: ${ip}
  gtpu:
    server:
      - address: ${ip}
  metrics:
    server:
      - address: ${ip}
        port: 9090
  session:
    - subnet: 10.45.0.0/16
    - subnet: 2001:db8:cafe::/48
  dns:
    - 8.8.8.8
    - 8.8.4.4
  mtu: 1400
EOF
            ;;
        upf)
            cat >> config/${component}.yaml << EOF
  pfcp:
    server:
      - address: ${ip}
    client:
      smf:
        - address: 10.45.0.12
  gtpu:
    server:
      - address: ${ip}
  session:
    - subnet: 10.45.0.0/16
    - subnet: 2001:db8:cafe::/48
  metrics:
    server:
      - address: ${ip}
        port: 9090
EOF
            ;;
        ausf|udm|nssf)
            cat >> config/${component}.yaml << EOF
      nrf:
        - uri: http://10.45.0.10:7777
      scp:
        - uri: http://10.45.0.10:7777
EOF
            ;;
        udr|pcf|bsf)
            cat >> config/${component}.yaml << EOF
      nrf:
        - uri: http://10.45.0.10:7777
db_uri: mongodb://mongodb/open5gs
EOF
            ;;
        hss)
            cat >> config/${component}.yaml << EOF
db_uri: mongodb://mongodb/open5gs
EOF
            ;;
    esac
}

# Créer les configurations pour chaque composant
create_config nrf 10.45.0.10
create_config amf 10.45.0.11
create_config smf 10.45.0.12
create_config upf 10.45.0.13
create_config ausf 10.45.0.14
create_config udm 10.45.0.15
create_config udr 10.45.0.16
create_config pcf 10.45.0.17
create_config nssf 10.45.0.18
create_config bsf 10.45.0.19
create_config hss 10.45.0.20

echo "✅ Fichiers de configuration créés dans ./config/"
