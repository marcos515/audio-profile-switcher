import os, json, logging

logging.basicConfig(level=logging.INFO)

MAIN_OUTPUT_ALIAS = 'JBL LIVE460NC'

HD_MODE = 'a2dp-sink'
HF_MODE = 'headset-head-unit'

def toggle_headset_mode(output_alias):
    run_command('rm output.json;pactl -fjson list sinks >> output.json')

    for device in get_devices():
        name = device['properties']['device.name']
        alias = device['properties'].get('device.alias', 'No Alias')
        logging.info(f'{name} - {alias}')

        if alias == output_alias:
            if device['active_port'] == 'headset-output':
                run_command(f'pactl set-card-profile {name} {HF_MODE}')
                logging.info(f'{alias} is now in {HF_MODE} mode')
            else:
                run_command(f'pactl set-card-profile {name} {HD_MODE}')
                logging.info(f'{alias} is now in {HD_MODE} mode')

def configure_headset(output_alias, mode):
    run_command('rm output.json;pactl -fjson list sinks >> output.json')

    for i, device in enumerate(get_devices()):
        index = device['index']
        name = device['properties']['device.name']
        alias = device['properties'].get('device.alias', 'No Alias')
        logging.info(f'{name} - {alias}')

        if alias == output_alias:
            run_command(f'pactl set-default-sink {index}')
            run_command(f'pactl set-card-profile {name} {mode}')
            logging.info(f'{alias} is now the default audio output device in {mode} mode')

def get_devices():
    data = []
    with open('output.json') as f:
        data = json.load(f)
    return data

def run_command(command):
    os.system(command)

if __name__ == "__main__":
    toggle_headset_mode(MAIN_OUTPUT_ALIAS)