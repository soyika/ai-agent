const mqtt = require('mqtt')

const MQTT_BROKER = process.env.MQTT_BROKER || 'mqtt://localhost:1883'
const MQTT_USERNAME = process.env.MQTT_USERNAME || 'kiwi_mqtt'
const MQTT_PASSWORD = process.env.MQTT_PASSWORD || 'kiwi_mqtt_password'
const MQTT_TOPIC_PREFIX = process.env.MQTT_TOPIC_PREFIX || 'kiwi/iot'
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api/v1'

const client = mqtt.connect(MQTT_BROKER, {
  username: MQTT_USERNAME,
  password: MQTT_PASSWORD,
  clientId: `kiwi_gateway_${Math.random().toString(16).slice(3)}`,
})

client.on('connect', () => {
  console.log('[IoT Gateway] Connected to MQTT broker')
  client.subscribe(`${MQTT_TOPIC_PREFIX}/sensor/#`)
  client.subscribe(`${MQTT_TOPIC_PREFIX}/device/#`)
  client.subscribe(`${MQTT_TOPIC_PREFIX}/control/#`)
})

client.on('message', async (topic, message) => {
  const payload = JSON.parse(message.toString())
  console.log(`[IoT Gateway] Received topic=${topic}, payload=`, payload)

  if (topic.startsWith(`${MQTT_TOPIC_PREFIX}/sensor/`)) {
    await forwardSensorData(payload)
  } else if (topic.startsWith(`${MQTT_TOPIC_PREFIX}/device/`)) {
    await handleDeviceEvent(payload)
  } else if (topic.startsWith(`${MQTT_TOPIC_PREFIX}/control/`)) {
    await handleControlCommand(payload)
  }
})

async function forwardSensorData(data) {
  try {
    const response = await fetch(`${API_BASE_URL}/iot/sensor`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) {
      console.error('[IoT Gateway] Failed to forward sensor data:', response.status)
    }
  } catch (error) {
    console.error('[IoT Gateway] Error forwarding sensor data:', error)
  }
}

async function handleDeviceEvent(data) {
  console.log('[IoT Gateway] Device event:', data)
}

async function handleControlCommand(data) {
  console.log('[IoT Gateway] Control command:', data)
  const { device_id, action, params } = data
  client.publish(`${MQTT_TOPIC_PREFIX}/device/${device_id}/response`, JSON.stringify({
    status: 'ok',
    action,
    timestamp: new Date().toISOString(),
  }))
}

client.on('error', (error) => {
  console.error('[IoT Gateway] MQTT error:', error)
})

console.log('[IoT Gateway] Starting Kiwifruit IoT Gateway...')
