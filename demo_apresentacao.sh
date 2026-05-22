#!/bin/bash
# Script Interativo para a Apresentação - Grupo 01 (Paravirtualização e KVM)
# Rodar este script na hora de apresentar para a banca!

# Definição de Cores para o Terminal
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}   SEMINÁRIO: VIRTUALIZAÇÃO NATIVA E PARAVIRTUALIZAÇÃO  ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "Bem-vindo ao ambiente de Provedor Regional (NaaS).\n"

# Passo 1: Prova do Isolamento de Rede
echo -e "${YELLOW}[PASSO 1] Pressione [ENTER] para mostrar o Isolamento de Rede (Open vSwitch)...${NC}"
read

echo -e "${GREEN}Executando: sudo ovs-vsctl show${NC}\n"
sudo ovs-vsctl show
echo -e "\n${CYAN}>> Note que as portas 'vnet0' e 'vnet1' estão isoladas no switch virtual 'br-data'.${NC}\n"

# Passo 2: Prova de funcionamento das VMs no Hypervisor
echo -e "${YELLOW}[PASSO 2] Pressione [ENTER] para listar as Máquinas Virtuais no Hypervisor KVM...${NC}"
read

echo -e "${GREEN}Executando: sudo virsh list --all${NC}\n"
sudo virsh list --all
echo ""

# Passo 3: Prova da Paravirtualização no KVM
echo -e "${YELLOW}[PASSO 3] Pressione [ENTER] para extrair a prova técnica de Paravirtualização (virtio)...${NC}"
read

echo -e "${GREEN}Executando a leitura do XML do libvirt para a VM 'cliente1'...${NC}"
echo -e "Filtrando por interfaces de rede e discos configurados para usar o barramento paravirtualizado:\n"
sudo virsh dumpxml cliente1 | grep -i virtio

echo -e "\n${CYAN}>> Os itens listados acima provam que a VM não está emulando hardware antigo, mas usando barramento 'virtio' nativo!${NC}\n"

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}   DEMONSTRAÇÃO AUTOMÁTICA CONCLUÍDA!   ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "Opcional: Para provar pelo lado do sistema convidado (Guest OS), acesse a VM com:"
echo -e "1. sudo virsh console cliente1"
echo -e "2. Faça o login (cirros / gocubsgo)"
echo -e "3. Digite: cat /sys/class/net/eth0/device/uevent"
