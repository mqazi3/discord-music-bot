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

| Category | Technologies |
|---|---|
| Language | Python |
| Discord | discord.py |
| Audio | yt-dlp, FFmpeg |
| Concurrency | asyncio |
| Containerization | Docker |
| AWS | ECS/Fargate, ECR, CloudWatch |

## Engineering Highlights

- Built an asynchronous, event-driven Python bot for Discord voice-channel interaction
- Implemented 8 commands plus event handlers for voice connection management, playback controls, and bot interaction
- Integrated `yt-dlp` with FFmpeg for audio source resolution and voice playback
- Used `asyncio` executor-based processing to keep blocking audio-source extraction from interfering with asynchronous bot operation
- Containerized the application with Docker and deployed it to AWS ECS/Fargate
- Troubleshot application dependencies, container runtime behavior, deployment configuration, and voice playback during cloud deployment

## Architecture

```text
Discord User
     |
     v
discord.py Bot
     |
     +----> Command & Event Handling
     |
     +----> yt-dlp
     |        |
     |        v
     +----> FFmpeg Audio Playback
     |
     v
Discord Voice Channel

Docker Image -> Amazon ECR
Bot Container -> AWS ECS/Fargate
Runtime Logs -> Amazon CloudWatch
```

## Commands

| Command | Function |
|---|---|
| `!join` | Connect the bot to the user's voice channel |
| `!leave` | Disconnect the bot from the voice channel |
| `!play` | Resolve an audio source and begin playback |
| `!pause` | Pause the current audio |
| `!resume` | Resume paused audio |
| `!stop` | Stop the current audio |
| `!hello` | Respond to a basic bot interaction |
| `!info` | Display bot information |

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
```

## Project Status

The AWS deployment is currently offline to avoid ongoing cloud infrastructure costs. The bot was previously deployed on AWS ECS/Fargate and operated across 2 Discord servers with 165+ combined members.
