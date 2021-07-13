# Denon AVR Serial Control over IP for Home Assistant

[![GitHub Stars](https://img.shields.io/github/stars/troykelly/hacs-denonavr3806.svg)](https://github.com/troykelly/hacs-denonavr3806/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/troykelly/hacs-denonavr3806.svg)](https://github.com/troykelly/hacs-denonavr3806/issues) [![Current Version](https://img.shields.io/badge/version-0.0.2-green.svg)](https://github.com/troykelly/hacs-denonavr3806) [![Validate](https://github.com/troykelly/hacs-denonavr3806/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/troykelly/hacs-denonavr3806/actions/workflows/validate.yml)

Control serial only or telnet Denon AVR devices like the Denon AVR3806 over IP with a serial to IP gateway.

## Zone control

The three zones of the AVR will appear as seperate media devices to control.

## Buy me a coffee

If this helps you, or you are just generous. I do love coffee.

<a href="https://buymeacoff.ee/troykelly" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

## Features

- Control all three Denon AVR Zones
- Control source input and volume

## Setup

Add the integration.

<img width="409" alt="HA_Denon_AVR_3806_Integration" src="https://user-images.githubusercontent.com/4564803/96110770-0b731080-0f2c-11eb-9c77-9cc98b209e7f.png">

Supply a name for the integration - or stick with the default if you are only going to add one.
Supply the hostname (or IP address) and port of your IP to serial gateway.

## Usage

Once connected, the three zones will appear with relevant controls.

## Contributions

PR's are more than welcome either to the HACS component or the Denon AVR Serial Library.
