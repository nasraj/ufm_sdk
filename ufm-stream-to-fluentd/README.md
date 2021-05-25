UFM stream To FluentD endpoint
--------------------------------------------------------


This plugin is used to extract topology via UFM API and stream it via [fluentd](https://www.fluentd.org/) protocol to telemetry console

Overview
--------------------------------------------------------

The UFM Enterprise product is Nvidia’s platform for IB fabric management. Through this platform, the various devices (switches, multi-chip systems, cables, etc.) are discovered, configured and the status of the entire fabric is reflected.
As a fabric manager, the UFM Enterprise holds an internal representation model of the network topology. This topology should be reflected, over time (as it can change with time) towards telemetry console. In order to do so, we present stream To FluentD plugin



Prerequisites 
--------------------------------------------------------

To install all prerequisites, please run :

    pip install -r requirements.txt

Run  
-------------------------------------------------------- 
### 1) using command line arguments :


    python ufm-stream-to-fluentd.py --fluentd_host=fluentd_host --fluentd_port=fluentd_port --ufm_host=ufm_host --ufm_username=ufm_username --ufm_protocol=https --ufm_password=ufm_password


### 2) using configuration file:
  
  - copy config file sample ufm-stream-to-fluentd.sample.cfg to ufm-stream-to-fluentd.cfg 
      
    
    cp ufm-stream-to-fluentd.sample.cfg ufm-stream-to-fluentd.cfg

  - Edit config file with relevant parameters 

    
    vi ufm-stream-to-fluentd.cfg

  - Run

    
    python ufm-stream-to-fluentd.py

 Running syntax
--------------------------------------------------------

| Argument | Corresponding Config Value | Required | Description | 
| :---: | :---: |:---: |:---: |
| --fluentd_host <fluentd_host> | [fluentd-config.host](ufm-stream-to-fluentd.sample.cfg#L25) | True |  Hostname or IP for FluentD endpoint
| --fluentd_port <fluentd_port> | [fluentd-config.port](ufm-stream-to-fluentd.sample.cfg#L26) | True | Port for FluentD endpoint  
| --ufm_host <ufm_host> | [ufm-remote-server-config.host](ufm-stream-to-fluentd.sample.cfg#L2) | True | Hostname or IP for The UFM Enterprise
| --ufm_server_name <ufm_server_name> | [ufm-remote-server-config.server_name](ufm-stream-to-fluentd.sample.cfg#L3) | True | Server name for The UFM Enterprise
| --ufm_protocol <ufm_protocol> | [ufm-remote-server-config.ws_protocol](ufm-stream-to-fluentd.sample.cfg#L5) | True | Web services protocol used by UFM Enterprise (HTTP, HTTPS)  
| --ufm_username <ufm_username> | [ufm-remote-server-config.username](ufm-stream-to-fluentd.sample.cfg#L7) | True | Username of UFM user
| --ufm_password <ufm_password> | [ufm-remote-server-config.password](ufm-stream-to-fluentd.sample.cfg#L8) | True | Password of UFM user
| --ufm_local_streaming <ufm_local_streaming> | [ufm-local-server-config.local_streaming](ufm-stream-to-fluentd.sample.cfg#L11) | False | If Enabled,the topology will be streamed from internal ufm server
| --internal_ufm_server_port <internal_ufm_server_port> | [ufm-local-server-config.internal_server_port](ufm-stream-to-fluentd.sample.cfg#L13) | False | Internal ufm server port [Required in case ufm_local_streaming is enabled (Default is 8000)]
| --logs_file_name <logs_file_name> | [logs-config.logs_file_name](ufm-stream-to-fluentd.sample.cfg#L30) | False | Log file name, if not provided a default stream wil lbe used
| --logs_level <logs_level> | [logs-config.logs_level](ufm-stream-to-fluentd.sample.cfg#L33) | False | Default is 'info'
| --streaming <streaming> | [streaming-config.streaming](ufm-stream-to-fluentd.sample.cfg#L16) | False | Enable/Disable topology streaming [Default is 'True']
| --streaming_interval <streaming_interval> | [streaming-config.interval](ufm-stream-to-fluentd.sample.cfg#L17) | False | The periodic interval [the script will be ran in every X minutes (Default is 5 minutes)]
| --streaming_systems <streaming_systems> | [streaming-config.systems](ufm-stream-to-fluentd.sample.cfg#L18) | False | Default is 'True'
| --streaming_ports <streaming_ports> | [streaming-config.ports](ufm-stream-to-fluentd.sample.cfg#L19) | False | Default is 'True'
| --streaming_links <streaming_links> | [streaming-config.links](ufm-stream-to-fluentd.sample.cfg#L20) | False | Default is 'True'
| --streaming_alarms <streaming_alarms> | [streaming-config.alarms](ufm-stream-to-fluentd.sample.cfg#L21) | False | Default is 'True'
| --daemon <daemon> | [streaming-config.run_as_daemon](ufm-stream-to-fluentd.sample.cfg#L22) | False | Runs the application as a daemon. Default is 'False'
   
*If command line argument is provided, the corresponding config value will be ignored

Use
-------------------------------------------------------- 
You can run this application as a daemon or run it via time-based job scheduler (cron job).
