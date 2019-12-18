from myiputils import read_ipv4_header
from mytcputils import *
import struct
from random import randint


def make_ipv4_header(size, src_addr, dest_addr, dscp=None, ecn=None, identification=None, flags=None, frag_offset=None, ttl=64, proto=None, verify_checksum=False):

    version = 4 << 4
    ihl = 5
    vihl = version | ihl

    if dscp is None:
        dscp = 0 << 6
    if ecn is None:
        ecn = 0

    dscpecn = dscp | ecn

    total_length = size + 20

    if identification is None:
        identification = randint(0, 2**16)

    if flags is None:
        flag_rsv = 0
        flag_dtf = 0
        flag_mrf = 0
        flags = (flag_rsv << 2) | (flag_dtf << 1) | (flag_mrf << 0)

    if frag_offset is None:
        frag_offset = 0

    flags <<= 13
    flags |= frag_offset

    if proto is None:
        proto = 6

    checksum = 0
    src_addr = str2addr(src_addr)
    dest_addr = str2addr(dest_addr)
    header = struct.pack('!BBHHHBBH', vihl, dscpecn, total_length, identification, flags, ttl, proto, checksum) + src_addr + dest_addr

    assert 4*ihl==20
    assert len(header) == 4*ihl
    checksum = calc_checksum(header)
    header = struct.pack('!BBHHHBBH', vihl, dscpecn, total_length, identification, flags, ttl, proto, checksum) + src_addr + dest_addr

    return header


def ip_to_binary(ip):
    octet_list_int = ip.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    binary = ("").join(octet_list_bin)
    return binary

def get_addr_network(address, net_size):
    ip_bin = ip_to_binary(address)
    network = ip_bin[0:32-(32-net_size)]
    return network

def ip_in_prefix(ip_address, prefix):
    [prefix_address, net_size] = prefix.split("/")
    net_size = int(net_size)
    prefix_network = get_addr_network(prefix_address, net_size)
    ip_network = get_addr_network(ip_address, net_size)
    return ip_network == prefix_network


def make_icmp(datagrama):

    tipo = 11
    code = 0
    unused = 0
    erro = datagrama[:28]
    checksum = calc_checksum(struct.pack('!BBI',tipo,code,unused)+ erro)
    icmp = struct.pack('!BBHI', tipo, code, checksum, unused) + erro
    return icmp


class CamadaRede:
    def __init__(self, enlace):
        """
        Inicia a camada de rede. Recebe como argumento uma implementação
        de camada de enlace capaz de localizar os next_hop (por exemplo,
        Ethernet com ARP).
        """
        self.callback = None
        self.enlace = enlace
        self.enlace.registrar_recebedor(self.__raw_recv)
        self.meu_endereco = None
        self.tabela = {}

    def __raw_recv(self, datagrama):
        dscp, ecn, identification, flags, frag_offset, ttl, proto, \
           src_addr, dst_addr, payload = read_ipv4_header(datagrama)
        if dst_addr == self.meu_endereco:
            if proto == 6 and self.callback:
                self.callback(src_addr, dst_addr, payload)
        else:
            if ttl - 1 > 0:
                next_hop = self._next_hop(dst_addr)
                header = make_ipv4_header(len(payload), src_addr, dst_addr, dscp, ecn, identification, flags, frag_offset, ttl-1, proto, True)
                print('\x1b[6;37;44m' + f"╔════════════════════════════════════╗")
                print('\x1b[6;37;44m' + f"║   {src_addr} -> {next_hop}   ║")
                self.enlace.enviar(header + payload, next_hop)
                print('\x1b[6;37;44m' + f"╚════════════════════════════════════╝")
            else:
                next_hop = self._next_hop(src_addr)
                size = 8 + 20 + min(8, len(payload))
                header = make_ipv4_header(size, self.meu_endereco, src_addr, dscp, ecn, identification, flags, frag_offset, 64, 1, True)
                icmp = make_icmp(datagrama)
                print('\x1b[7;31;47m' + f"╔════════════════════════════════════╗")
                print('\x1b[7;31;47m' + f"║Devolvendo pacote -> {next_hop}  ║")
                self.enlace.enviar(header + icmp, next_hop)
                print('\x1b[7;31;47m' + f"╚════════════════════════════════════╝")




    def _get_subnet(self, dest_addr):
        candidatos = []
        for v,_ in self.tabela.items():
            if ip_in_prefix(dest_addr, v):
                candidatos.append(v)
        while len(candidatos) > 1:
            for c1 in candidatos:
                for c2 in candidatos:
                    if c1 != c2:
                        if ip_in_prefix(c2.split("/")[0], c1):
                            if c1 in candidatos:
                                candidatos.remove(c1)
        if candidatos:
            return self.tabela[candidatos[0]]

    def _next_hop(self, dest_addr):
        # TODO: Use a tabela de encaminhamento para determinar o próximo salto
        # (next_hop) a partir do endereço de destino do datagrama (dest_addr).
        # Retorne o next_hop para o dest_addr fornecido.
        ip = self._get_subnet(dest_addr)
        return ip

    def definir_endereco_host(self, meu_endereco):
        """
        Define qual o endereço IPv4 (string no formato x.y.z.w) deste host.
        Se recebermos datagramas destinados a outros endereços em vez desse,
        atuaremos como roteador em vez de atuar como host.
        """
        self.meu_endereco = meu_endereco

    def definir_tabela_encaminhamento(self, tabela):
        """
        Define a tabela de encaminhamento no formato
        [(cidr0, next_hop0), (cidr1, next_hop1), ...]

        Onde os CIDR são fornecidos no formato 'x.y.z.w/n', e os
        next_hop são fornecidos no formato 'x.y.z.w'.
        """
        tabela_aux = {}

        for t in tabela:
            tabela_aux[t[0]] = t[1]

        self.tabela = tabela_aux

        # TODO: Guarde a tabela de encaminhamento. Se julgar conveniente,
        # converta-a em uma estrutura de dados mais eficiente.

    def registrar_recebedor(self, callback):
        """
        Registra uma função para ser chamada quando dados vierem da camada de rede
        """
        self.callback = callback

    def enviar(self, segmento, dest_addr):
        """
        Envia segmento para dest_addr, onde dest_addr é um endereço IPv4
        (string no formato x.y.z.w).
        """
        next_hop = self._next_hop(dest_addr)
        datagrama = make_ipv4_header(len(segmento), self.meu_endereco, dest_addr) + segmento
        # TODO: Assumindo que a camada superior é o protocolo TCP, monte o
        # datagrama com o cabeçalho IP, contendo como payload o segmento.
        self.enlace.enviar(datagrama, next_hop)
