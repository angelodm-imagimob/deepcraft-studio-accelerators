# Live Data Collection

## Overview

This project records live audio from a microphone into a Dataset. The graph in `Main.imunit` contains two nodes:

- **Microphone** streams audio from a local input device. Output is normalized float32 samples, one value per channel.
- **Dataset** stores the stream as a data track in `datasets/Main_1.dcdb`. The track is created when the Microphone is connected to the Dataset.

Nothing sits between the two nodes, so the recorded audio is the raw microphone signal.

## Microphone settings

Select the Microphone node and set these in the Properties panel:

| Setting | Options | Default |
|---------|---------|---------|
| Device | Audio input devices found on this computer (Device 0 to 3) | Device 0 |
| Sample rate | 8 kHz, 16 kHz, 44.1 kHz, 48 kHz | 16 kHz |
| Channels | Mono, Stereo | Mono |

The sample rate is stored with the recorded track. Use the rate your model expects when you train on this data.

If no device is found at the selected index, recording fails with "Unable to find recording device. Check selected device." Pick another device and record again.

## Record data

1. Open `Main.imunit` from the Solution Explorer and check the Microphone settings.
2. Open the Dataset node to show its sessions and timeline.
3. Create a new recording with **Record New** in the Sessions tab. Studio prepares the recording, which can take a few moments.
4. When preparation is done, the take waits. Recording starts only when you press **Record** on the timeline, so you choose the exact start moment.
5. Use **Pause** and **Resume** during the take if needed.
6. Press **Stop** to finish. The audio is saved in the Dataset.

To replace an existing take, select it and press **Record** on the timeline, confirm the prompt, then press **Record** again once preparation is done. The old take is replaced only if the new recording stops cleanly.

## Add labels (optional)

The graph has no label track. To annotate recordings, add a label track in the Dataset and label the audio on the timeline. Define the labels that fit your use case.

## Learn more

Read more about building ML graphs: https://developer.imagimob.com/getting-started/graph-ux-concept.
