class CamadaEnlace:
    def __init__(self, linhas_seriais):
        self.enlaces = {}
        for ip_outra_ponta, linha_serial in linhas_seriais.items():
            enlace = Enlace(linha_serial)
            self.enlaces[ip_outra_ponta] = enlace
            enlace.registrar_recebedor(self.callback)

    def registrar_recebedor(self, callback):
        self.callback = callback

    def enviar(self, datagrama, next_hop):
        try:
            self.enlaces[next_hop].enviar(datagrama)
        except:
            pass


    def callback(self, datagrama):
        if self.callback:
            self.callback(datagrama)


class Enlace:
    def __init__(self, linha_serial):
        self.linha_serial = linha_serial
        self.linha_serial.registrar_recebedor(self.__raw_recv)
        self.buffer = []
        self.result = ''
        self.callback = None

    def registrar_recebedor(self, callback):
        self.callback = callback

    def enviar(self, datagrama):
        datagrama = datagrama.replace(b"\xdb", b"\xdb\xdd").replace(b"\xc0", b"\xdb\xdc")
        datagrama = b'\xc0' + datagrama + b'\xc0'
        print(f"║       Enviando pacote SLIP         ║")
        self.linha_serial.enviar(datagrama)

    def __raw_recv(self, dados):
        dados = dados.hex()

        for i in range(0, len(dados), 2):
            cursor = dados[i] + dados[i + 1]
            if cursor != 'c0':
                if cursor != '':
                    self.buffer.append(cursor)

            if cursor == 'c0' and self.buffer:
                while self.buffer:
                    if type(self.result) is bytes:
                        self.result = self.result.hex() + self.buffer.pop(0)
                    self.result = self.result + self.buffer.pop(0)

                self.result = bytes(bytearray.fromhex(self.result))
                self.result = self.result.replace(b"\xdb\xdc", b"\xc0").replace(b"\xdb\xdd", b"\xdb")
                try:
                    self.callback(self.result)
                except:
                    import traceback
                    traceback.print_exc()
                self.result = ''
