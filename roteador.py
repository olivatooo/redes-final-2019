#!/usr/bin/env python3
import asyncio
from camadafisica import ZyboSerialDriver
from myip import CamadaRede      # copie o arquivo da Etapa 3
from myslip import CamadaEnlace  # copie o arquivo da Etapa 4


driver = ZyboSerialDriver()

serial1 = driver.obter_porta(2)
pty1 = driver.expor_porta_ao_linux(3)

serial2 = driver.obter_porta(4)
pty2 = driver.expor_porta_ao_linux(5)

serial3 = driver.obter_porta(6)
pty3 = driver.expor_porta_ao_linux(7)

print()
print('sudo slattach -vLp slip {}'.format(pty1.pty_name))
print('sudo slattach -vLp slip {}'.format(pty2.pty_name))
print('sudo slattach -vLp slip {}'.format(pty3.pty_name))
print()


# Os endereços IP que especificamos abaixo são os endereços da outra ponta do
# enlace. No caso do teste montado de acordo as mensagens acima, são os
# endereços atribuídos às interface de rede do Linux.
enlace = CamadaEnlace({'192.168.123.1': serial1,
                       '192.168.124.1': serial2,
                       '192.168.125.1': serial3})

rede = CamadaRede(enlace)

# Este é o endereço IP do nosso roteador. Como os enlaces são ponto-a-ponto,
# ele não precisa estar em uma mesma subrede que os endereços IP atribuídos
# às interfaces do Linux.
rede.definir_endereco_host('192.168.122.1')

# A tabela de encaminhamento define através que qual enlace o nosso
# roteador pode alcançar cada faixa de endereços IP.
rede.definir_tabela_encaminhamento([
    ('192.168.123.0/24', '192.168.123.1'),
    ('192.168.124.0/24', '192.168.124.1'),
    ('192.168.125.0/24', '192.168.125.1'),
])


asyncio.get_event_loop().run_forever()
