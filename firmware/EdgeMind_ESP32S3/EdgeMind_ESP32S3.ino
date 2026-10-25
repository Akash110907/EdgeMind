/*
  EdgeMind — ESP32-S3 On-Chip Edge AI Processing
  Starter firmware · Vishwakarma Awards 2026-27 (App ID: VK26-IITI-AHM-0463)
  Team: Akash S, Pranov Bhalaji AV, SenthilKumaran J

  STATUS: Phase 1 starter.
    - I2S mic capture: baseline retained
    - Wi-Fi send to companion device: baseline retained
    - TFLite Micro inference: NOT IMPLEMENTED. runInference() below is an
      amplitude-threshold placeholder, not a trained ML model.
      See /model/README.md for the integration requirements.

  Hardware: ESP32-S3 DevKitC-1 N16R8 + INMP441 I2S MEMS mic + battery
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include "driver/i2s.h"
#include "secrets.h"   // WIFI_SSID, WIFI_PASSWORD, SERVER_URL — copy from secrets.h.example

// ---------- I2S mic pins (INMP441) — change to match your wiring ----------
#define I2S_SCK_PIN   2    // Bit clock
#define I2S_WS_PIN    15   // Word select / L-R clock
#define I2S_SD_PIN    13   // Serial data out of the mic
#define I2S_PORT      I2S_NUM_0

#define SAMPLE_RATE      16000
#define BUFFER_SAMPLES   512

static int32_t rawBuffer[BUFFER_SAMPLES];
static int16_t pcmBuffer[BUFFER_SAMPLES];

void setupWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }
  Serial.print("\nWiFi connected: ");
  Serial.println(WiFi.localIP());
}

void setupI2SMic() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = BUFFER_SAMPLES,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK_PIN,
    .ws_io_num = I2S_WS_PIN,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD_PIN
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

// Reads one chunk of audio and converts the mic's 32-bit I2S frames to 16-bit PCM.
size_t readAudioChunk() {
  size_t bytesRead = 0;
  i2s_read(I2S_PORT, rawBuffer, sizeof(rawBuffer), &bytesRead, portMAX_DELAY);
  size_t samplesRead = bytesRead / sizeof(int32_t);
  for (size_t i = 0; i < samplesRead; i++) {
    pcmBuffer[i] = (int16_t)(rawBuffer[i] >> 14);  // INMP441: top 18 bits carry the data
  }
  return samplesRead;
}

// ---------------------------------------------------------------------
// PLACEHOLDER ONLY — this is NOT machine-learning inference.
// Before replacing it:
//   1. Add a real, compatible .tflite model or generated C array.
//   2. Add the matching audio frontend/feature extraction. The standard
//      micro_speech model expects its features, not raw pcmBuffer samples.
//   3. Add an ESP32-S3-compatible TFLite Micro runtime and register the
//      operators required by the selected model.
//   4. Validate tensor shapes, quantization, memory, and outputs on-device.
// Keep the I2S capture and Wi-Fi POST path intact while doing so.
// ---------------------------------------------------------------------
String runInference(int16_t* samples, size_t count) {
  if (count == 0) return "silence";
  int64_t energy = 0;
  for (size_t i = 0; i < count; i++) energy += abs(samples[i]);
  float avgEnergy = (float)energy / count;
  return avgEnergy > 500 ? "sound_detected" : "silence";
}

void sendResult(const String& result) {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  http.begin(SERVER_URL);  // e.g. http://<phone-or-laptop-ip>:5000/result
  http.addHeader("Content-Type", "application/json");
  String payload = "{\"device\":\"edgemind-esp32s3\",\"result\":\"" + result + "\"}";
  int code = http.POST(payload);
  Serial.printf("POST -> %d\n", code);
  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(500);
  setupWiFi();
  setupI2SMic();
  Serial.println("EdgeMind ready — listening...");
}

void loop() {
  size_t n = readAudioChunk();
  if (n > 0) {
    String result = runInference(pcmBuffer, n);
    Serial.println(result);
    sendResult(result);
  }
}
