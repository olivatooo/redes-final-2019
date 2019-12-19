# Roteador Juninho

Este repositório contém uma implementação simplificada de um roteador que utiliza os protolocos IP e SLIP para comunicação. A implementação física do roteador foi feita em uma placa Zybo Z7-20, para mais informações veja o arquivo `HowTo.md`.
Grupo que realizou esse projeto:
* Esther Hoffmann
* @Danchlax
* @igmagollo

Toda a implementação from scratch foi feita com orientação, paciência e ajuda de @thotypous.

# IP

O arquivo myip.py contém a implementação do protoloco IP. Todas as funções estão em apenas um arquivo mas seria interessante a separação dessas funções em arquivos diferentes para a melhor organização.

Nesta implementação estaremos utilizando uma tabela de encaminhamento fixa para a `camada de rede`, ao instanciar a classe CamadaRede deve-se atribuir uma tabela de encaminhamento para ela operar.

Na função __raw_recv nota-se que podemos atuar:
* Host
  * dst_addr == self.meu_endereco
* Roteador
  * Encaminhar pacote
    *  ttl - 1 > 0
  * Devolver pacote (ICMP).

# SLIP

O arquivo myslip.py contém a implementação do [protocolo SLIP](https://en.wikipedia.org/wiki/Serial_Line_Internet_Protocol) um protoloco de comunicação super simples de ser implementado! Ele é utilizado como `camada de enlace`.

# Problemas

A implementação atual é bloqueante! Ou seja, ao enviar ou receber dados no `myslip.py` ou no `myip.py` os programas bloqueiam toda a pipeline até que toda o recebimento ou envio seja feito. No caso da `camada física` apenas o envio é bloqueante.

# Debugging

Após diversos testes para a utilização física do roteador os seguintes comandos foram de grande ajuda para encontrar problemas na comunicação entre duas pontas.

```
sudo tcpdump -vnX -i sl0
```

```
sudo ip netns exec ns1 tcpdump -vnX -i sl1
```

```
sudo ip netns exec ns2 tcpdump -vnX -i sl2
```
