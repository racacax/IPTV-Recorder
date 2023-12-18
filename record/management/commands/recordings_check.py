import datetime
import logging
import os
import subprocess
import threading
from os import path

import requests
from django.core.management.base import BaseCommand
import time

from django.utils import timezone
from django.utils.text import slugify

from record.models import Recording
from django.conf import settings

RUNNING_IDS = {}


def launch_command(command_str: str, recording: Recording, type:str):
    with open(recording.writing_directory + "logs.txt", 'a') as f:
        logging.warning(f"{recording} launched")
        command = subprocess.Popen("exec " + command_str, stdin=subprocess.PIPE,
                                   stderr=f, shell=True)
        RUNNING_IDS[recording.id] = command
        command.command_type = type
        while command.poll() is None:
            time.sleep(0.5)
        logging.warning(f"{recording} exited")
        if recording.id in RUNNING_IDS:
            del RUNNING_IDS[recording.id]


def launch_wget(recording: Recording, name: str):
    if '"' in name or '"' in recording.selected_source.url:  # prevent XSS
        return
    launch_command(f'wget --user-agent="{settings.USER_AGENT}" "{recording.selected_source.url}" -O "{name}"',
                   recording, "wget")


def launch_ffmpeg(recording: Recording, name: str):
    if '"' in name or '"' in recording.selected_source.url:  # prevent XSS
        return
    launch_command(f'{settings.FFMPEG_PATH} -user_agent "{settings.USER_AGENT}" -i "{recording.selected_source.url}" -c copy "{name}"',
                   recording, "ffmpeg")


def start_recording(recording: Recording):
    if len(recording.video_sources.all()) == 0:
        return
    RUNNING_IDS[recording.id] = None
    if not path.exists(recording.writing_directory):
        os.mkdir(recording.writing_directory)
    if recording.selected_source is None:
        recording.selected_source = recording.video_sources.all().first()
    elif recording.consecutive_retries >= recording.use_backup_after:
        recording.consecutive_retries = 0
        ids = [v.id for v in recording.video_sources.all()]
        recording.selected_source = recording.video_sources.all()[
            (ids.index(recording.selected_source.id) + 1) % len(ids)]

    recording.last_retry = datetime.datetime.now(tz=timezone.get_current_timezone())
    recording_method = recording.selected_source.recording_method
    name = recording.writing_directory + slugify(recording.name + " - " + recording.last_retry.strftime("%Y-%m-%d "
                                                                                                        "%H:%M:%S")) + ".mp4"
    if recording_method == "wget":
        threading.Thread(target=launch_wget, args=[recording, name]).start()
    elif recording_method == "ffmpeg":
        threading.Thread(target=launch_ffmpeg, args=[recording, name]).start()
    recording.consecutive_retries += 1
    recording.total_retries += 1
    recording.save()


def stop_recording(recording: Recording):
    try:
        process: subprocess.Popen = RUNNING_IDS[recording.id]
        if recording.id in RUNNING_IDS:
            del RUNNING_IDS[recording.id]
        if process.command_type == "ffmpeg":
            process.communicate(input="q".encode("utf-8"))
            time.sleep(30) # we allow ffmpeg 30s maximum to finish encoding job
            if process.poll() is None:
                process.terminate()
        else:
            process.terminate()
    except Exception as e:
        logging.exception(f"{e}")


class Command(BaseCommand):
    help = "Check Recordings"

    def handle(self, *args, **options):
        while True:
            current_date = datetime.datetime.now(tz=timezone.get_current_timezone())
            for recording in Recording.objects.exclude(id__in=RUNNING_IDS).filter(start_time__lte=current_date,
                                                                                  end_time__gt=current_date).prefetch_related(
                "video_sources").select_related("selected_source"):
                try:
                    start_recording(recording)
                except Exception as e:
                    logging.exception(f"{e}")
            for recording in Recording.objects.filter(id__in=RUNNING_IDS, end_time__lte=current_date):
                stop_recording(recording)
            time.sleep(1)
