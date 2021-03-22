# EDMC-AutoLoader
Plugin for [Elite Dangerous Market Connector](https://github.com/EDCD/EDMarketConnector) to launch additional tools alongside the app on startup.

I primarily use AutoLoader to start external applications such as 
[ED Engineer](https://github.com/msarilar/EDEngineer) and [Elite-Dangerous-X52-MFD](https://github.com/AZaps/Elite-Dangerous-X52-MFD) without
having to resort to event viewer editing on Windows.

## Installation and Usage
**WARNING:** This plugin does not verify the authenticity of any files it opens.
It is up to you to ensure you monitor your load list and only auto-launch files you trust.

1. Download the latest release from the releases page.
2. Extract the folder on top of any existing files in your EDMC plugins directory.
3. Run EDMC, open the settings, and in the "AutoLoader" tab, add a list of executables you want to run.
4. The next time EDMC runs it will load the specified files in order.

AutoLoader does not track running apps and hence will not close them when EDMC shuts down.

## Acknowledgements
- [Elite Dangerous Market Connector](https://github.com/EDCD/EDMarketConnector)
- [Elite Dangerous Community Developers Discord](https://discord.com/invite/usQ5e6n)
## License
Copyright © 2020-2021 Neo Ting Wei Terrence

Licensed under the GNU Public License (GPL) version 3 or later.
