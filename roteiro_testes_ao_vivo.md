# ⚡ Roteiro de Testes ao Vivo (Para a Apresentação)

Este roteiro contém comandos rápidos para você copiar e colar durante a sua apresentação oficial. O objetivo é causar alterações na infraestrutura em tempo real para provar à banca que o **Dashboard** e o KVM estão interligados.

**Pré-requisito:** 
1. Deixe o seu painel web rodando em um terminal (`sudo python3 dashboard.py`).
2. Abra uma **SEGUNDA** janela do terminal do Ubuntu (ou aba do WSL) para rodar os comandos abaixo.
3. Posicione o navegador e o terminal lado a lado na tela.

---

## 1. Testando o Compute Plane (Falhas em VMs)

Esses comandos alteram diretamente o estado do KVM. Após rodar qualquer um deles, clique no botão "Atualizar Dados" no Dashboard.

### Pausar uma Máquina Virtual (Simulando congelamento de processo/snapshot)
```bash
sudo virsh suspend cliente2
```
👉 *No Dashboard: O status do `cliente2` mudará para **paused**.*

### Retomar a Máquina Virtual 
```bash
sudo virsh resume cliente2
```
👉 *No Dashboard: O status do `cliente2` voltará para **running**.*

### Desligar uma Máquina Virtual Abruptamente (Simulando queda de energia do host)
```bash
sudo virsh destroy cliente1
```
👉 *No Dashboard: O status do `cliente1` mudará para **shut off**.*

### Ligar a Máquina Virtual Novamente (Retomando operações)
```bash
sudo virsh start cliente1
```
👉 *No Dashboard: O status do `cliente1` voltará para **running**.*

---

## 2. Testando o Data Plane (Reação do Switch Virtual)

O Open vSwitch é feito para cenários dinâmicos de nuvem (SDN). Vamos provar isso na prática.

### Conectar uma "Nova Porta" Fictícia (Simula plugar um novo cabo no switch)
```bash
sudo ovs-vsctl add-port br-data vnet-teste-01
```
👉 *No Dashboard: A porta `vnet-teste-01` aparecerá magicamente conectada na topologia do Open vSwitch.*

### Desconectar a Porta Imediatamente
```bash
sudo ovs-vsctl del-port br-data vnet-teste-01
```
👉 *No Dashboard: A porta sumirá da lista, demonstrando a programabilidade de redes.*
