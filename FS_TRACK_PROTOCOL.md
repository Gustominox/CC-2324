# FS TRACK PROTOCOL SYNTAX

Qualquer linha que comece por '#' é considerado um comentario e por isso ignorada na mensagem
Qualquer linha em branco deve ser ignorada

```markdown
# NODE_ID 
IP=senderIp
# HEADER
MSGTYPE=UPDATE NODE
# BODY
FILE1 SEG=[...] SIZE
FILE2 SEG=[...] SIZE
FILE3 SEG=[...] SIZE
```

```markdown
# HEADER
FILES LIST
# BODY
```
