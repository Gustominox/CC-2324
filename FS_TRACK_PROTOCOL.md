# FS TRACK PROTOCOL SYNTAX

Qualquer linha que comece por '#' é considerado um comentario e por isso ignorada na mensagem
Qualquer linha em branco deve ser ignorada

tipos de mensagens:

"UPDATE NODE"

"DELETE NODE"

"FILES LIST"

"END TRACKER"


```markdown
# NODE_ID 
SENDER_ID=senderIp
# HEADER
MSG_TYPE=UPDATE NODE
# BODY
BODY={
FILE1 SEG=[...] SIZE,
FILE2 SEG=[...] SIZE,
FILE3 SEG=[...] SIZE
}
```

```markdown
# HEADER
FILES LIST
# BODY
```
