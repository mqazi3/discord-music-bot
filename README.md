# Discord Music Bot

An asynchronous Discord music bot built with Python, discord.py, yt-dlp, FFmpeg, Docker, and AWS ECS/Fargate.

## Overview

Discord Music Bot is an event-driven Python application that connects to Discord voice channels and provides command-based audio playback. The bot uses `discord.py` for Discord integration, `yt-dlp` for resolving audio sources, and FFmpeg for voice playback.

The application was containerized with Docker and deployed to AWS ECS/Fargate, with container images stored in Amazon ECR and runtime logs monitored through Amazon CloudWatch. The bot was used across 2 Discord servers with 165+ combined members.

## Features

- Asynchronous, event-driven command handling with `discord.py`
- Discord voice-channel connection and audio playback
- Audio source extraction and streaming using `yt-dlp` and FFmpeg
- Playback controls for play, pause, resume, and stop
- Commands for joining and leaving voice channels
- Concurrent audio-source processing using Python's `asyncio` executor
- Dockerized application runtime
- AWS ECS/Fargate deployment with images stored in Amazon ECR
- Runtime and deployment monitoring through Amazon CloudWatch logs

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
