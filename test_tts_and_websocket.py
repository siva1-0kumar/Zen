import asyncio
import websockets
import json
import logging
from exotel_websocket_server import TTSService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_tts_service():
    tts = TTSService()
    sample_text = "This is a test of the ElevenLabs TTS API."
    audio_bytes = tts.generate_speech(sample_text)
    if audio_bytes:
        logger.info(f"TTS API returned audio bytes of length: {len(audio_bytes)}")
    else:
        logger.error("TTS API failed to return audio bytes")

async def test_websocket_events(uri):
    async with websockets.connect(uri) as websocket:
        # Send connected event
        await websocket.send(json.dumps({"event": "connected"}))
        logger.info("Sent connected event")

        # Send start event
        await websocket.send(json.dumps({
            "event": "start",
            "start": {"from": "+1234567890", "to": "+0987654321"}
        }))
        logger.info("Sent start event")

        # Send media event with parameters to trigger TTS
        media_event = {
            "event": "media",
            "stream_sid": "test_stream",
            "sequence_number": 1,
            "media": {
                "chunk": 1,
                "timestamp": "1000",
                "payload": ""  # empty payload for test
            },
            "parameters": {
                "response_text": "Hello from test websocket client"
            }
        }
        await websocket.send(json.dumps(media_event))
        logger.info("Sent media event with TTS parameters")

        # Receive response
        response = await websocket.recv()
        logger.info(f"Received response: {response}")

        # Send stop event
        await websocket.send(json.dumps({"event": "stop"}))
        logger.info("Sent stop event")

async def main():
    # Test TTS API
    await test_tts_service()

    # Test websocket server events
    websocket_uri = "ws://localhost:8765"  # <-- Changed from 8777 to 8765
    await test_websocket_events(websocket_uri)

if __name__ == "__main__":
    asyncio.run(main())
