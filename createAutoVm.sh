#!/bin/bash
# Script de création et installation automatique d'une VM Ubuntu 22.04 avec VirtualBox (mode headless)

VM_NAME="Ubuntu898989"
ISO_PATH="$HOME/Downloads/ubuntu-22.04.3-desktop-amd64.iso"
VM_DIR="$HOME/VirtualBox VMs/$VM_NAME"
DISK_PATH="$VM_DIR/${VM_NAME}.vdi"
RAM=10048
CPUS=4
DISK_SIZE=100000   # en Mo (20 Go)

USERNAME="user"
PASSWORD="password123"
FULLNAME="Ubuntu User"

echo "=== Création de la VM $VM_NAME (headless) ==="

# Créer la VM
VBoxManage createvm --name "$VM_NAME" --ostype Ubuntu_64 --register

# Configurer la VM
VBoxManage modifyvm "$VM_NAME" \
  --memory $RAM \
  --cpus $CPUS \
  --nic1 nat \
  --graphicscontroller vmsvga \
  --audio none

# Créer un disque dur
VBoxManage createmedium disk --filename "$DISK_PATH" --size $DISK_SIZE

# Ajouter un contrôleur SATA
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci

# Attacher le disque dur
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" \
  --port 0 --device 0 --type hdd --medium "$DISK_PATH"

# Installation non interactive avec VBoxManage (mode headless)
VBoxManage unattended install "$VM_NAME" \
  --iso="$ISO_PATH" \
  --user="$USERNAME" \
  --full-user-name="$FULLNAME" \
  --password="$PASSWORD" \
  --locale="fr_FR" \
  --time-zone="Europe/Paris" \
  --hostname="${VM_NAME}.local" \
  --install-additions \
  --start-vm=headless

echo "=== Installation automatique en cours... (VM en arrière-plan) ==="
echo "➡️ Tu peux vérifier l'état avec : VBoxManage showvminfo \"$VM_NAME\""
echo "➡️ Pour ouvrir la console : VBoxManage startvm \"$VM_NAME\" --type gui"
