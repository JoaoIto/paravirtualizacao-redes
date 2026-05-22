Relatório Técnico: Virtualização Nativa e Paravirtualização em Infraestruturas Modernas

1. Objetivos e Escopo do Seminário

Este seminário, conduzido pelo Grupo 01, tem como propósito dissecar as camadas de abstração de hardware sob a perspectiva de um arquiteto de infraestrutura. O foco central reside na análise comparativa entre a Virtualização Completa (muitas vezes referida no contexto de hardware atual como Virtualização Nativa) e a Paravirtualização, avaliando como essas escolhas impactam a escalabilidade e a resiliência dos serviços de TI.

Os objetivos fundamentais deste estudo compreendem:

* Analisar as distinções fundamentais entre virtualização completa e paravirtualização, com foco em mecanismos de comunicação guest-hypervisor.
* Avaliar as arquiteturas dos hypervisors KVM e Xen, identificando suas abordagens distintas para o gerenciamento de recursos.
* Mensurar os impactos técnicos da virtualização nos pilares de desempenho, latência e densidade de recursos (CPU/Memória).
* Explorar a aplicação de redes virtualizadas sob o modelo Network as a Service (NaaS) em ambientes de alta demanda.
* Estruturar um projeto prático para a modernização de um Provedor Regional de Internet através de infraestrutura virtualizada.

2. Fundamentação Teórica: Virtualização Completa vs. Paravirtualização

A virtualização moderna evoluiu do isolamento lógico para uma integração profunda com o silício. A "Virtualização Nativa" contemporânea é essencialmente a Virtualização Assistida por Hardware (Intel VT-x / AMD-V), que permite a execução de instruções privilegiadas sem modificação no kernel do convidado.

Característica	Virtualização Completa (Full Virtualization)	Paravirtualização (Para-Virtualization)
Interação com o Hardware	Utiliza Binary Translation ou suporte de hardware (Intel VT-x) para emular o set de instruções.	O SO convidado é modificado para enviar comandos diretamente ao hypervisor via Hypercalls.
Sistema Operacional Convidado	Unaware: O SO não sabe que está virtualizado e opera como se estivesse em bare-metal.	Aware: O SO tem consciência da camada de virtualização, otimizando o caminho de execução.
Abstração de E/S (I/O)	Depende de emulação total de dispositivos (via QEMU, por exemplo), o que pode gerar maior overhead.	Utiliza drivers paravirtualizados (como VirtIO) para bypass de emulação, reduzindo a latência de I/O.

3. Análise de Arquitetura: KVM vs. Xen

Como especialistas em infraestrutura, devemos distinguir como esses hypervisors se posicionam em relação ao hardware e ao sistema operacional host:

* Arquitetura:
  * KVM (Kernel-based Virtual Machine): Frequentemente classificado como um Hypervisor Tipo-2 que atua como Tipo-1. Ele é um módulo do kernel Linux que transforma o próprio SO host em um hypervisor. O KVM delega a emulação de hardware de entrada/saída ao QEMU, enquanto o escalonamento de tarefas e o gerenciamento de memória são realizados nativamente pelo kernel Linux.
  * Xen: É um hypervisor bare-metal (Tipo-1) autêntico que reside em uma camada inferior ao sistema operacional. Ele inicializa um domínio privilegiado chamado Dom0, uma máquina virtual com acesso direto ao hardware que gerencia os drivers e orquestra os domínios não privilegiados (DomU).
* Diferenças Chave: A principal divergência técnica reside no gerenciamento do plano de controle. Enquanto o KVM se beneficia da vasta compatibilidade de drivers do kernel Linux moderno, o Xen oferece um isolamento mais rigoroso através de seu microkernel, sendo a referência histórica em implementações de paravirtualização pura, embora hoje ambos suportem modos híbridos (PVH).

4. Métricas de Desempenho e Eficiência

A abstração de recursos impõe penalidades técnicas que devem ser mitigadas através de tuning arquitetural. Os três pilares de análise são:

1. Desempenho Geral: Impactado diretamente pelo Context Switching (troca de contexto) entre o modo usuário do guest, o kernel do guest e o hypervisor. A eficiência aqui depende da redução dessas transições.
2. Latência: Sensível ao I/O Overhead. Em ambientes de missão crítica, a latência de rede e disco é o principal gargalo, exigindo o uso de anéis de memória compartilhada (Ring Buffers) para transferência de dados.
3. Uso de CPU e Memória: A eficiência na alocação envolve o gerenciamento de Overcommitment e técnicas de Memory Ballooning, permitindo que o hypervisor recupere memória não utilizada de VMs ociosas para redistribuir em picos de carga.

5. Virtualização Aplicada a Redes (NaaS)

No contexto de Provedores de Internet, o Network as a Service (NaaS) transcende a simples criação de VLANs. Ele se fundamenta em SDN (Software Defined Networking) para abstrair o plano de controle do plano de dados. Através da virtualização de funções de rede (NFV), um provedor pode provisionar dinamicamente serviços de VPLS (Virtual Private LAN Service) ou SD-WAN para clientes corporativos, garantindo escalabilidade programática sem a necessidade de intervenção física em racks e switches.

6. Caso Prático: Provedor Regional de Internet

Propomos a transição de uma infraestrutura monolítica para uma arquitetura virtualizada, visando alta disponibilidade.

* Cenário e Justificativa: O provedor necessita consolidar serviços para reduzir custos operacionais (OPEX).
  * Justificativa Técnica: Recomenda-se a Virtualização Completa (Hardware-Assisted) para sistemas legados de faturamento onde não há acesso ao kernel. Para serviços de alto throughput, recomenda-se a Paravirtualização (ou drivers PV em KVM) para garantir desempenho próximo ao bare-metal.
* Arquitetura do Sistema: A topologia consiste em clusters de hosts físicos com armazenamento compartilhado. As VMs serão segmentadas por criticidade, incluindo serviços essenciais como:
  * DNS Recursivo e Autoritativo: (Isolamento para segurança).
  * Servidores Radius: (Autenticação de usuários).
  * Sistemas de Cache e Borda: (Otimização de tráfego). A rede virtual será estruturada em pontes (bridges) e switches virtuais suportando segmentação por VXLAN para futura expansão NaaS.
* Componentes de Entrega:
  * [ ] Diagrama: Topologia lógica detalhando o fluxo de dados entre Dom0/Host e as VMs.
  * [ ] Justificativa Técnica: Documento validando a escolha entre KVM e Xen com base no overhead de I/O tolerável.
  * [ ] Protótipo: Ambiente funcional demonstrando o isolamento de recursos.

7. Metodologia e Restrições Técnicas do Protótipo

Para assegurar a viabilidade do projeto, o protótipo deve respeitar diretrizes de arquitetura de classe carrier:

1. Isolamento de Planos: Deve ser demonstrada a separação clara entre o Management Plane (acesso administrativo ao Host/Dom0) e o Data Plane (tráfego das máquinas virtuais).
2. Otimização de I/O: É mandatório o uso de drivers paravirtualizados no protótipo para comprovar a redução de latência em serviços de rede.
3. Consistência: A justificativa técnica deve estar estritamente alinhada às métricas de desempenho discutidas na Seção 4, provando que a arquitetura escolhida suporta a carga de trabalho projetada para um ISP regional.
