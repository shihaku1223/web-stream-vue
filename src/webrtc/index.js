function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

const id = uuidv4()
const HELLO_TOKEN = 'HELLO'
let nodeStatus = undefined

const constraints = {
  video: true, audio: false
}

const sendHello = (ws) => {
  console.log(id)
  ws.send(HELLO_TOKEN + ' ' + id)
}

const getPeerId = () => {
  return id
}



const onServerMessage = (ev) => {
  console.log(ev.data)

  switch(ev.data) {
    case HELLO_TOKEN:
      return
  }

  try {
    message = JSON.parse(ev.data)
  } catch(e) {
    console.log('Parse JSON data error.')
    return
  }

  if(message.sdp) {
    console.log('got sdp')
  }
}

const onServerError = (ev) => {
}

const connectToSignalingServer = (address) => {

  const ws = new WebSocket(address)

  ws.addEventListener('open', (ev) => {
    sendHello(ws)
  })
  ws.addEventListener('message', onServerMessage)
  ws.addEventListener('error', onServerError)
  ws.addEventListener('close', (ev) => {
  })
}

const getLocalStream = () => {

  if(navigator.mediaDevices.getUserMedia) {
    return navigator.mediaDevices.getUserMedia(constraints)
  }
}

export {
  getLocalStream,
  connectToSignalingServer,
  getPeerId,
}
