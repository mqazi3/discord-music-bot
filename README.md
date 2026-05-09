# Discord Music Bot

Cloud-hosted Discord music bot built with Python, Docker, and AWS ECS/Fargate.

## Overview

This project is a containerized Discord music bot that supports asynchronous command handling and voice-channel audio playback. The bot was deployed to AWS using ECS/Fargate, with Docker image storage in ECR and runtime monitoring through CloudWatch logs.

## Features

- Discord bot command handling
- Voice-channel connection support
- YouTube/audio playback support
- Asynchronous event-driven processing
- Dockerized application deployment
- AWS ECS/Fargate cloud hosting
- AWS ECR image management
- CloudWatch logging for deployment/debugging

## Tech Stack

- Python
- discord.py
- yt-dlp
- ffmpeg
- Docker
- AWS ECS/Fargate
- AWS ECR
- AWS CloudWatch

## Project Structure

```text
discord-music-bot/
  MusicBot1.py
  Dockerfile
  requirements.txt
  .dockerignore
  .env.example
  .gitignore
  README.md