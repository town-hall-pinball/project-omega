# External Dependencies

This directory contains scripts needed to build and install
dependecies for the P-ROC. This should work on the following
platforms:

* Ubuntu, Precise 64-bit
* Raspbian

## Installation

To download and install the pre-built binaries, run the following:

```bash
./download-dependencies
sudo ./install-run-dependencies
```

## Auto Build and Install

To build and install everything from scratch, run the following:

```bash
./build-all
```

`sudo` will be invoked as needed to install packages.

## Manual Build and Install

To build and install each package manually, install the build
dependencies first:

```bash
sudo ./install-run-dependencies
```

and then run the following:

```bash
make -f <package>.mk
sudo ./local-stow dist/<package>.*.tar.gz
```

Example:

```bash
make -f libusb.mk
sudo ./local-stow dist/libusb.*.tar.gz
```
