# Model integration notes

## Current state

No model asset is checked into this folder yet. The firmware's current `runInference()` function is an amplitude-threshold placeholder, not TensorFlow Lite Micro (TFLM) inference. Do not treat `sound_detected` / `silence` as ML predictions.

## Choosing the model

The TensorFlow Lite Micro `micro_speech` example is a small **keyword-spotting** demo, commonly trained for “yes” and “no” with “unknown” and “silence” handling. It is useful for validating a keyword-spotting pipeline, but it is not a defence audio-event classifier for gunshots, artillery, helicopter/rotor noise, or sirens. Those require a model trained and evaluated for the target sound classes.

Use the model and frontend from the same example/version. The standard micro_speech model does **not** accept arbitrary raw PCM samples as its input; it expects the audio features produced by its matching frontend. A model with a different input tensor shape, quantization, or feature pipeline cannot be substituted without adapting the firmware.

## Integration checklist

1. Choose the intended task and label set. For a first smoke test, use the official TensorFlow Lite Micro micro_speech example; for EdgeMind's eventual sound-event task, train/obtain a model for those target classes.
2. Confirm the model's license, input/output tensor shapes, tensor types, quantization scales/zero-points, required operators, and flash/RAM footprint.
3. Add the actual converted `.tflite` asset or generated C array/header here. Keep large/generated files and provenance documented; do not create a dummy model or claim an asset is present when it is not.
4. Integrate a compatible ESP32-S3 TFLM runtime (for example, a maintained Arduino-compatible port) and register every operator required by the selected model.
5. Implement the **matching audio frontend** (for micro_speech, the expected feature extraction; not direct PCM-to-tensor copying).
6. Feed the feature tensor, invoke the interpreter, and map the output tensor to documented labels using the model's quantization parameters.
7. Test with known positive, negative, silence, and noisy recordings. Measure recognition quality, latency, and peak memory on the actual ESP32-S3.
8. Only mark the model/inference checklist complete after the firmware compiles, runs on hardware, and passes recorded tests.

## Why the model is not included here yet

The current repository archive contains no model file. This README intentionally documents the integration contract rather than embedding an unverified or mismatched model. The microphone capture and Wi-Fi POST code should remain unchanged while the inference path is developed and tested separately.
