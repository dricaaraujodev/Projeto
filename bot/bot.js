import zmq from "zeromq";

function nowISO() {
  return new Date().toISOString();
}

async function runBot() {
  const sock = new zmq.Request();
  await sock.connect("tcp://server:5555");
  console.log("🤖 Bot connected to server");

  const name = "bot_js_" + Math.floor(Math.random() * 1000);
  const login = { service: "login", data: { user: name, timestamp: nowISO() } };
  await sock.send(JSON.stringify(login));
  const [reply] = await sock.receive();
  console.log("Login reply:", reply.toString());

  const usersReq = { service: "users", data: { timestamp: nowISO() } };
  await sock.send(JSON.stringify(usersReq));
  const [usersReply] = await sock.receive();
  console.log("Users reply:", usersReply.toString());

  // keep the bot alive for debugging purposes
  setInterval(async () => {
    const ping = { service: "users", data: { timestamp: nowISO() } };
    await sock.send(JSON.stringify(ping));
    const [r] = await sock.receive();
    console.log("Heartbeat users:", r.toString());
  }, 15000);
}

runBot().catch(err => console.error(err));
