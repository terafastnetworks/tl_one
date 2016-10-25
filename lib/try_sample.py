import socket

class SocketHandler:

  def __init__(self, sock=None):
    print "inside __init__ function........"
    if sock is None:
      self.sock = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.sock = sock

  def connect(self):
    print "inside connect function........."
    self.sock.connect(('10.99.99.225', 3082))

  def send(self, msg):
    print "inside send function........."
    totalsent = 0
    MSGLEN = len(msg)
    while totalsent < MSGLEN:
      sent = self.sock.send(msg)
      print "sent : ", sent
      if sent == 0 :
        raise RuntimeError("socket connection broken")

      totalsent = totalsent + sent
      print "totalsent :", totalsent

  def receive(self, EOFChar='\036'):
    print "inside receive function........."
    msg = ''
    MSGLEN = 100
    while len(msg) < MSGLEN:
      chunk = self.sock.recv(MSGLEN-len(msg))
      print "chunk : ", MSGLEN-len(msg)
      print "chunk.find(EOFChar)", chunk.find(EOFChar)
      if chunk.find(EOFChar) != -1:
        msg = msg + chunk
        print "msg :", msg
        return msg

      msg = msg + chunk
      print "msg :", msg
      return msg


tl1 = SocketHandler()

tl1.connect()
tl1.send('act-user::admin:123::root;')
tl1.receive()
tl1.send('RTRV-EQPT::9999:123:::PARAMETER=SIZE;')
tl1.receive()
tl1.send('RTRV-USER-SECU:::123:;')
tl1.receive()
tl1.send('')
tl1.receive()
