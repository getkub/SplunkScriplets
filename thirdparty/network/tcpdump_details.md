# https://gist.github.com/tuxfight3r/9ac030cb0d707bb446c7
```
                     TCPDUMP FLAGS
URG  =  (Not Displayed in Flag Field, Displayed elsewhere) 
ACK  =  (Not Displayed in Flag Field, Displayed elsewhere)
PSH  =  [P] (Push Data)
RST  =  [R] (Reset Connection)
SYN  =  [S] (Start Connection)
FIN  =  [F] (Finish Connection)
SYN-ACK =  [S.] (SynAcK Packet)
[.] (No Flag Set)
```

Sending a 'hello' to port 514 (shell) from source-port 56916
```
09:26:22.019275 IP localhost.56916 > localhost.shell: Flags [S], seq 2913462468, win 43690, options [mss 65495,sackOK,TS val 3064249342 ecr 0,nop,wscale 7], length 0
09:26:22.019293 IP localhost.shell > localhost.56916: Flags [S.], seq 3342840827, ack 2913462469, win 43690, options [mss 65495,sackOK,TS val 3064249342 ecr 3064249342,nop,wscale 7], length 0
09:26:22.019306 IP localhost.56916 > localhost.shell: Flags [.], ack 1, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 0
09:26:22.019362 IP localhost.56916 > localhost.shell: Flags [P.], seq 1:7, ack 1, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 6
09:26:22.019370 IP localhost.shell > localhost.56916: Flags [.], ack 7, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 0
09:26:22.019389 IP localhost.56916 > localhost.shell: Flags [F.], seq 7, ack 1, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 0
09:26:22.019509 IP localhost.shell > localhost.56916: Flags [F.], seq 1, ack 8, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 0
09:26:22.019525 IP localhost.56916 > localhost.shell: Flags [.], ack 2, win 342, options [nop,nop,TS val 3064249342 ecr 3064249342], length 0
```
