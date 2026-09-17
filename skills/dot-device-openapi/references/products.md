# Products and hardware resources

Choose the device's documented integration route before requesting credentials or preparing a Canvas payload. Hardware capabilities do not imply Dot cloud API support.

| Product | Hardware and use | Integration route |
| --- | --- | --- |
| Quote/0 (摘录) | 2.66-inch e-paper; the public Canvas layout baseline is 296 × 152 | Dot device APIs for supported, bound devices; [Open Platform hardware resources](https://github.com/MindReset/dot_open_platform/tree/main/devices/quote_0) for custom firmware |
| Rand/0 (口袋先知) | 1.54-inch, 200 × 200 e-paper; buttons, motion interaction, and NFC features | Device-local functions and LAN Display Mode; not Dot App binding or Dot cloud APIs |
| Read/0 (Pico in Chinese, Read series / 小纸) | ESP32-S3; 4.7-inch native 16-level grayscale e-paper; two-point touch and three touch keys; 8 MB PSRAM, 16 MB Flash; replaceable 2050 mAh battery, microSD, USB-C | Official demo firmware and custom firmware development; do not assume cloud APIs or Canvas delivery are available |

## Read/0 / Pico

- [Product documentation](https://dot.mindreset.tech/docs/read_0)
- [Official demo guide](https://dot.mindreset.tech/docs/read_0/start)
- [Build and flash](https://dot.mindreset.tech/docs/read_0/firmware)
- [Open Platform resource entry](https://github.com/MindReset/dot_open_platform/tree/main/devices/read_0)
- [Official firmware repository](https://github.com/MindReset/read_pico_firmware)

The official factory demo covers display refresh, reading tests, touch, acceleration, power, storage, fonts, and sleep/wake behavior. The repository includes the board support, chip drivers, and pinout. It currently requires ESP-IDF v6.1 and targets ESP32-S3. Follow its own build instructions and component licenses. Keep firmware sources in that repository rather than embedding them in this skill.

The panel resolution is 1216 × 684 in the firmware reference. Confirm orientation, framebuffer order, and refresh mode in the firmware before composing a screen; do not treat the physical panel dimensions as a Canvas API size selector.

## Rand/0

- [Product documentation](https://dot.mindreset.tech/docs/rand_0)
- [Getting started](https://dot.mindreset.tech/docs/rand_0/start)
- [Display Mode resource entry](https://github.com/MindReset/dot_open_platform/tree/main/capabilities/rand_0_display_mode)
- [Local protocol](https://github.com/MindReset/dot_open_platform/blob/main/capabilities/rand_0_display_mode/protocol.md)
- [Official browser example](https://github.com/MindReset/dot_open_platform/blob/main/capabilities/rand_0_display_mode/examples/web/display_ws_test.html)

The published Display Mode reference targets firmware 1.3.1. Complete Wi-Fi Time Sync first, put the computer and device on the same trusted LAN, then open Main menu → More → Display on the device. Use the shown IP address with the official browser example. It supports 200 × 200 black-and-white or four-level grayscale frames and receives button events. Long-press the top button to leave Display Mode.

Display Mode has no additional login authentication and accepts one active client. Do not expose the device port to the internet. Use the documented local protocol rather than Dot API keys, cloud device IDs, or Canvas sending scripts.

## Design versus delivery

The information hierarchy and e-paper design guidance in `dot-canvas-designer` can inform all three products. Its JSON schema and sending tools are specific to the public Canvas API. Rand/0 Display Mode expects image frames; Read/0 firmware development follows the firmware repository's rendering interfaces. Do not promise either device accepts `windowData` directly.
