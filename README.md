# MeteoAlarm

[![HACS Custom][hacs_badge]][hacs_url]
[![GitHub Release][releases_badge]][releases_url]
[![License][license_badge]][license_url]

> **Note**: This is a **custom integration** for Home Assistant that provides enhanced functionality over the built-in MeteoAlarm integration. This version includes a modern configuration flow for easier setup.

The MeteoAlarm custom integration allows you to watch for weather alerts in Europe from [MeteoAlarm](https://www.meteoalarm.org/) (EUMETNET). This integration creates a binary sensor that shows whether there are active weather warnings for your location.

## Features

- ✅ Easy setup via Home Assistant configuration flow
- ✅ Real-time weather alerts from MeteoAlarm
- ✅ Support for all European countries covered by MeteoAlarm
- ✅ Detailed alert information as attributes
- ✅ Custom naming of the binary sensor
- ✅ Multiple language support

## Installation

### Using HACS (Recommended)

1. Add this repository to HACS custom repositories:
   - Go to HACS → Settings → Custom repositories
   - Add `https://github.com/briis/meteoalarm`
   - Category: `Integration`

2. Install the MeteoAlarm integration from HACS

3. Restart Home Assistant

### Manual Installation

1. Clone or download this repository
2. Copy the `custom_components/meteoalarm` folder to your `custom_components` folder
3. Restart Home Assistant

## Configuration

The MeteoAlarm integration uses a modern configuration flow and does **not** require manual YAML configuration.

### Setup via Configuration Flow

1. Go to Settings → Devices & Services
2. Click "Create Automation" or look for MeteoAlarm in the integrations list
3. Click "Create Config Entry"
4. Fill in the following information:
   - **Country**: The full name of your country in English format (lowercase)
   - **Province**: The province/region name
   - **Language**: ISO language code (optional, default: `en`)
   - **Name**: Custom name for the binary sensor (optional, default: `meteoalarm`)

### Finding Your Country and Province

- Country: Use the full English name in lowercase (e.g., `netherlands`, `italy`, `germany`)
- Province: Get the exact province name from [MeteoAlarm Feeds](https://feeds.meteoalarm.org/)
- You can also use the [MeteoAlarm EMMA_ID Region explorer tool](https://saratoga-weather.org/meteoalarm-map/)

## Binary Sensor Attributes

When an alert is active, the binary sensor will have the following attributes:

```yaml
attribution: Information provided by MeteoAlarm
language: en-GB
category: Met
event: Severe weather warning
responseType: Monitor
urgency: Immediate
severity: Severe
certainty: Likely
effective: 2026-04-12T10:00:00+00:00
onset: 2026-04-12T10:00:00+00:00
expires: 2026-04-12T18:00:00+00:00
senderName: MeteoAlarm
headline: Orange weather warning
description: Severe weather expected in your region
instruction: Please follow local authorities' guidance
awareness_level: 3; orange; Severe
awareness_type: Weather
unit_of_measurement: null
friendly_name: meteoalarm
icon: mdi:alert
```

### Awareness Levels

- **2**: Yellow - Moderate
- **3**: Orange - Severe
- **4**: Red - High

## Usage Examples

### Automation: Alert on New Warning

```yaml
automation:
  - alias: "Alert me about weather warnings"
    triggers:
      - trigger: state
        entity_id: binary_sensor.meteoalarm
        from: "off"
        to: "on"
    actions:
      - service: notify.notify
        data:
          title: "{{ state_attr('binary_sensor.meteoalarm', 'headline') }}"
          message: |
            {{ state_attr('binary_sensor.meteoalarm', 'description') }}
            Effective: {{ state_attr('binary_sensor.meteoalarm', 'effective') }}
```

### Template Sensor: Display Alert Level

```yaml
template:
  - sensor:
      - name: "MeteoAlarm Level"
        unique_id: meteoalarm_level
        state: "{{ state_attr('binary_sensor.meteoalarm', 'awareness_level') }}"
        icon: mdi:alert
```

### Lovelace Card Example

```yaml
type: entities
entities:
  - entity: binary_sensor.meteoalarm
    name: Weather Alert
show_header_toggle: false
```

## Information Sources

To use this integration, you will need:

1. **Country and Province**: Available from [MeteoAlarm Feeds](https://feeds.meteoalarm.org/)
2. **Language Code**: ISO 639-1 codes (e.g., `en`, `nl`, `de`, `it`)
3. **Region Explorer**: [MeteoAlarm EMMA_ID Region explorer tool](https://saratoga-weather.org/meteoalarm-map/)

## Troubleshooting

### Invalid Country or Province
- Ensure the country name is spelled exactly as it appears in the MeteoAlarm feeds
- Double-check the province name for typos
- Use the region explorer tool to find the correct name

### No Alerts Showing
- Verify that your country and province combination exists in MeteoAlarm
- Check that there are actual alerts for your location at [MeteoAlarm](https://www.meteoalarm.org/)

### Language Not Available
- Not all languages are available for all countries
- The integration uses the language parameter to fetch alerts in that language
- Fall back to English (`en`) if your language is not supported

## Disclaimer

> ⚠️ **Important**: This integration is not affiliated with MeteoAlarm and retrieves data from the website by using the XML feeds. Use it at your own risk. The developers are not responsible for any missed warnings or incorrect data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

[hacs_badge]: https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge
[hacs_url]: https://hacs.xyz/
[releases_badge]: https://img.shields.io/github/release/briis/meteoalarm?style=for-the-badge
[releases_url]: https://github.com/briis/meteoalarm/releases
[license_badge]: https://img.shields.io/badge/license-MIT-blue?style=for-the-badge
[license_url]: ./LICENSE
