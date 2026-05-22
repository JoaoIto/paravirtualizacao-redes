# 🛠️ Guia de Bolso: Comandos do Laboratório KVM / OVS

Este guia concentra todos os comandos utilizados no projeto, divididos por categoria, para rápida consulta durante o seminário.

---

## 👁️ 1. Comandos de Informação e Monitoramento (Apenas Leitura)
Estes comandos não alteram a infraestrutura, apenas exibem logs, status e detalhes do ambiente.

| Comando | O que faz? |
| :--- | :--- |
| `sudo virsh list --all` | Lista todas as máquinas virtuais criadas e mostra se estão `running` (rodando), `paused` (pausadas) ou `shut off` (desligadas). |
| `sudo virsh dominfo cliente1` | Exibe um resumo dos recursos alocados para a VM (quanta CPU e Memória RAM ela está consumindo agora). |
| `sudo virsh nodeinfo` | Exibe a capacidade física do seu computador hospedeiro (Bare Metal), mostrando núcleos de CPU e Memória totais. |
| `sudo ovs-vsctl show` | Mostra a topologia do switch virtual em tempo real, listando a bridge (`br-data`) e quais portas/cabos (`vnet0`, `vnet1`) estão conectados nela. |
| `sudo python3 dashboard.py` | Inicia o servidor Web que grupa todas essas informações em uma interface visual atualizada a cada 2 segundos. |
| `sudo virsh dumpxml cliente1` | Exibe o código-fonte XML completo de como a VM foi construída no KVM (ótimo para procurar configurações `virtio`). |

---

## ⚡ 2. Comandos de Ação e Controle (Alteram a Infraestrutura)
Estes comandos agem ativamente na infraestrutura, ligando, desligando ou modificando recursos em tempo real.

| Comando | O que faz? |
| :--- | :--- |
| `sudo virsh start cliente1` | **LIGA** a máquina virtual caso ela esteja desligada (`shut off`). O KVM recria a interface de rede no Switch automaticamente. |
| `sudo virsh destroy cliente1` | **DESLIGA ABRUPTAMENTE** a máquina virtual (equivale a puxar da tomada). Usado para simular falhas severas. |
| `sudo virsh suspend cliente2` | **PAUSA (CONGELA)** a máquina virtual. A máquina para de processar na CPU, mas a memória RAM é mantida intacta. |
| `sudo virsh resume cliente2` | **RETOMA** a máquina virtual pausada. Ela volta a processar exatamente de onde parou. |
| `sudo virsh setmem cliente1 131072 --live` | **BALLOONING (DIMINUIR):** Rouba memória RAM da VM em tempo real (reduzindo para 128MB) usando o driver paravirtualizado, sem reiniciar a máquina. |
| `sudo virsh setmem cliente1 262144 --live` | **BALLOONING (AUMENTAR):** Devolve a memória RAM para a VM (voltando para 256MB) instantaneamente. |
| `sudo ovs-vsctl add-port br-data teste1` | **REDE:** Conecta um novo cabo/porta (chamado `teste1`) no switch virtual. |
| `sudo ovs-vsctl del-port br-data teste1` | **REDE:** Desconecta e exclui o cabo/porta do switch virtual. |

---

## 💻 3. Acesso Interno e Paravirtualização (Dentro do Guest OS)
Comandos para entrar na máquina e interagir diretamente com o kernel do cliente.

* **Para acessar o monitor da VM:**
  ```bash
  sudo virsh console cliente1
  ```
  *(Aperte `ENTER`, use o login `cirros` e a senha `gocubsgo`)*

* **Para extrair a prova da Paravirtualização de E/S (I/O):**
  ```bash
  cat /sys/class/net/eth0/device/uevent
  ```
  *(A saída `DRIVER=virtio_net` atesta que a VM se comunica diretamente com o Host e não usa hardware emulado).*

* **Para sair da VM e voltar ao Ubuntu:**
  Aperte `Ctrl + ]` (Control e fecha colchetes ao mesmo tempo).
