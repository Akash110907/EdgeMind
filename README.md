# EdgeMind — ESP32-S3 Edge Processing Prototype

Vishwakarma Awards 2026–27 submission · App ID: **VK26-IITI-AHM-0463**

**Team:** Akash S · Pranov Bhalaji AV · SenthilKumaran J

## Overview

EdgeMind is a planned battery-powered ESP32-S3 device for on-device audio analysis. The current firmware is an early prototype: it captures audio from an INMP441 I²S MEMS microphone, applies a simple amplitude threshold, and sends the resulting status string to a configured HTTP endpoint over Wi-Fi.

**Important status note:** the current `runInference()` function is only an amplitude-threshold placeholder. It is **not machine-learning inference**, does not classify sound events or keywords, and must not be presented as a trained TinyML model. Phone/laptop-to-device text or voice input is not implemented. The physical wiring and full end-to-end operation have **not yet been verified on the actual board**.

## Current data flow

```text
CURRENT
[INMP441 microphone] -- I²S --> [ESP32-S3 audio capture]
                                      |
                               amplitude threshold
                                      |
                         "sound_detected" / "silence"
                                      |
                            Wi-Fi HTTP POST
                                      v
                         [Configured server endpoint]

PLANNED (not implemented)
[Phone/laptop] -- text or voice over Wi-Fi --> [ESP32-S3]
```

## Hardware

- ESP32-S3 DevKitC-1 N16R8 (16 MB flash / 8 MB PSRAM)
- INMP441 I²S MEMS microphone
- LiPo battery with a suitable charger and protection circuit (integration pending)

## Software

- Arduino IDE
- Espressif `arduino-esp32` board package
- ESP32 I²S driver
- `WiFi.h` and `HTTPClient.h`
- TensorFlow Lite Micro (planned; not yet integrated)

## Repository layout

```text
firmware/EdgeMind_ESP32S3/
  EdgeMind_ESP32S3.ino
  secrets.h.example
model/
  README.md
```

## Status

- [x] Firmware starter and repository documentation
- [x] I²S microphone-capture code baseline
- [x] Wi-Fi HTTP POST-out code baseline
- [ ] Verify microphone wiring and audio capture on the physical board
- [ ] Select and integrate a trained model suitable for the target sound classes
- [ ] Implement the audio preprocessing expected by the selected model
- [ ] Implement phone/laptop input to the ESP32-S3
- [ ] Complete enclosure and battery/power integration
- [ ] Measure and document accuracy, latency, memory use, and reliability on hardware

The checked-in firmware reads chunks at a configured 16 kHz sample rate and currently returns `sound_detected` or `silence` based on average absolute sample amplitude. These strings are **not ML predictions**.

## Build and flash the current prototype

1. Install Arduino IDE and install **esp32 by Espressif Systems** using Boards Manager.
2. Open `firmware/EdgeMind_ESP32S3/EdgeMind_ESP32S3.ino`.
3. In the same folder, copy `secrets.h.example` to a local file named `secrets.h`.
4. Edit the local `secrets.h` with your Wi-Fi SSID, Wi-Fi password, and the HTTP endpoint that will receive the POST request. Do not commit this local file.
5. Select **ESP32S3 Dev Module**, choose the correct serial port, upload the sketch, and open Serial Monitor at **115200 baud**.
6. Confirm the intended pinout and power requirements against your specific board and microphone before connecting power. The pin assignments below are firmware defaults, not a claim that the physical wiring has been verified.

### INMP441 pin defaults in the current sketch

| INMP441 signal | ESP32-S3 GPIO / pin |
|---|---|
| SCK / BCLK | GPIO 2 |
| WS / LRCL | GPIO 15 |
| SD / DOUT | GPIO 13 |
| VDD | 3V3 |
| GND | GND |
| L/R | GND (left channel selection) |

Change the sketch's pin definitions if your wiring differs. Check the board and microphone documentation before powering the circuit.

### HTTP result payload

The sketch posts JSON similar to the following to `SERVER_URL`:

```json
{"device":"edgemind-esp32s3","result":"sound_detected"}
```

The receiver/server is external to this repository and must be running at the configured endpoint. The current firmware sends results outward; it does not run a listener for phone/laptop input.

## TinyML model plan

No trained model asset is currently integrated. The standard TensorFlow Lite Micro `micro_speech` example is a keyword-spotting demo, commonly using “yes” and “no” with “unknown” and “silence” handling. It is not a defence sound-event detector. A model for the intended target classes must be selected or trained, and the matching feature-extraction pipeline, tensor details, required operators, and memory requirements must be implemented and tested.

See [model/README.md](model/README.md) for the model integration checklist. Raw PCM samples must not be passed directly to a model that expects frontend-generated audio features.

## Security

- Keep real Wi-Fi credentials and private configuration only in the local `firmware/EdgeMind_ESP32S3/secrets.h` file.
- Commit `secrets.h.example` only; never commit `secrets.h`.
- The repository's `.gitignore` excludes `secrets.h`, but ignore rules do not remove a file that was already tracked.
- The visible commit history was checked for a tracked file named `secrets.h`; none was found. If any real password or token was shared elsewhere or exposed in another form, rotate it anyway.
- Use only a trusted network for testing; the sample HTTP endpoint is not encrypted with HTTPS.
