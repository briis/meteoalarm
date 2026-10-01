# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026.10.0] - Unreleased

### Fixed

- Fixed hassfest validation error by loosening the `meteoalertapi` requirement from `==0.3.1` to `>=0.3.1` in `manifest.json`.

### Changed

- Bumped Home Assistant dev dependency from `2026.8.0b0` to `2026.9.4`.
- Bumped `pytest-homeassistant-custom-component` from `0.13.349` to `0.13.367`.
- Bumped `ruff` from `0.16.1` to `0.16.9` ([#66](https://github.com/briis/meteoalarm/pull/66)).
- Pinned `pip` to `>=26.2.1,<26.3`.
- Bumped `home-assistant/actions/hassfest` GitHub Action ([#41](https://github.com/briis/meteoalarm/pull/41), [#65](https://github.com/briis/meteoalarm/pull/65)).
- Added devcontainer lock file.

## [2026.8.0] - 2026-08-04

### Changed

- Added copyright headers to all integration modules and fixed linting errors.
- Bumped Home Assistant dev dependency from `2026.5.1` to `2026.8.0b0`.
- Replaced `pytest` and `pytest-asyncio` with `pytest-homeassistant-custom-component` (`0.13.349`) in the dev requirements.
- Bumped `aiohasupervisor` requirement from `>=0.4.3` to `>=0.6.0` ([#17](https://github.com/briis/meteoalarm/pull/17)).
- Bumped `ruff` from `0.15.12` to `0.16.1` ([#18](https://github.com/briis/meteoalarm/pull/18), [#24](https://github.com/briis/meteoalarm/pull/24), [#29](https://github.com/briis/meteoalarm/pull/29)).
- Bumped `pip` requirement from `>=26.1.1` to `>=26.2` ([#16](https://github.com/briis/meteoalarm/pull/16)).
- Bumped `colorlog` from `6.10.1` to `6.12.0`.
- Bumped `actions/checkout` from 6 to 7.0.1 ([#23](https://github.com/briis/meteoalarm/pull/23), [#34](https://github.com/briis/meteoalarm/pull/34)).
- Bumped `actions/setup-python` from 6.2.0 to 7.0.0 ([#27](https://github.com/briis/meteoalarm/pull/27), [#33](https://github.com/briis/meteoalarm/pull/33)).
- Bumped `home-assistant/actions` GitHub Actions ([#19](https://github.com/briis/meteoalarm/pull/19), [#26](https://github.com/briis/meteoalarm/pull/26), [#35](https://github.com/briis/meteoalarm/pull/35)).

## [2026.5.0] - 2026-05-14

### Added

- Possibility to change the configuration after initial setup.
- Danish translation.

### Changed

- Bumped `pip` requirement from `>=21.3.1` to `>=26.1.1` ([#10](https://github.com/briis/meteoalarm/pull/10)).
- Bumped `ruff` from `0.15.10` to `0.15.12` ([#9](https://github.com/briis/meteoalarm/pull/9)).
- Bumped `aiohasupervisor` requirement from `>=0.4.0` to `>=0.4.3` ([#6](https://github.com/briis/meteoalarm/pull/6)).

[2026.10.0]: https://github.com/briis/meteoalarm/compare/2026.8.0...main
[2026.8.0]: https://github.com/briis/meteoalarm/compare/v2026.5.0...2026.8.0
[2026.5.0]: https://github.com/briis/meteoalarm/compare/v2026.4...v2026.5.0
