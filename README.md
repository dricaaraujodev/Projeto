# BBS Chat (Parte 1) - REQ/REP

Serviços:
- server (Python + ZeroMQ REP + SQLite) - escuta em tcp:5555
- client (Go + ZeroMQ REQ) - executa operações: login, users, channel, channels
- bot (Node.js + ZeroMQ REQ) - bot automático de teste

## Como rodar (Codespaces / Docker)
1. Abra o repo no Codespaces (ou local com Docker).
2. Build + up:
   ```bash
   docker compose up --build

3. Logs:

server ficará em background aguardando requests.

client executa os exemplos e finaliza (veja logs do container).

bot fica executando e faz heartbeat.
Para executar cliente manualmente (se necessário):
docker compose run --rm client
Verificar banco SQLite:
# no host (Codespace)
sqlite3 server/db.sqlite3 "SELECT * FROM users;"
sqlite3 server/db.sqlite3 "SELECT * FROM channels;"
Formato das mensagens (JSON)

Exemplos (REQ):

{ "service": "login", "data": { "user": "alice", "timestamp": "2025-11-11T20:00:00Z" } }
{ "service": "users", "data": { "timestamp": "2025-11-11T20:00:00Z" } }
{ "service": "channel", "data": { "channel": "geral", "timestamp": "2025-11-11T20:00:00Z" } }
{ "service": "channels", "data": { "timestamp": "2025-11-11T20:00:00Z" } }
Exemplos (REP) seguem o padrão do enunciado.

Branches sugeridas

main

part1-req-rep (esta implementação)

part2-pub-sub

part3-messagepack

part4-clocks

part5-replication

ui