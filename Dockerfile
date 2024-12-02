FROM ubuntu:20.04

# Set the environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    git \
    software-properties-common

# Copy the requirements file
RUN pip install fake_headers>=1.0.2 pandas>=2.0.3 python-dotenv>=1.0.0 selenium>=4.12.0 webdriver_manager>=4.0.0 openai

# Install firefox and geckodriver
RUN add-apt-repository ppa:mozillateam/ppa
RUN apt-get update
RUN echo 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n' > /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
RUN apt-get install -y firefox