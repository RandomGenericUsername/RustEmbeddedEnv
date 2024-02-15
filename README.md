# Aim

This project generates a docker image suitable for Rust embedded development.

Also provides a project creator to quickly initiate Rust projects wrapping around ```cargo-generate```

# Supported mcu

While the environment is suitable for developing for any target mcu, the project creator only supports a few mcu families/boards/models:

- STM32h755ZI
- STM32F411RE
- STM32WL55JC

# Prerequisites

Install the following:

- Make
- Docker

# Generating the image 


1. Pull from repo...
2. 

# config.yaml
Configuration for building the docker image.

## Mandatory keys
- host

### host:
Sets the architecture of the host machine.

#### usage:

```yaml
host: <host_machine_architecture>
```
Possible values for <host_machine_architecture>:
- amd64
- aarch64