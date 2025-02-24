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

RUNNING_IDS = {}

def format_str(base_str: str, replace_key: str, replace_value: str) -> str:
    replace_value.replace('\\', '').replace('"', '\"')
    return base_str.replace('{'+replace_key+'}', replace_value)

def launch_command(command_str: str, recording: Recording, termination_string :str):
    with open(recording.writing_directory + "logs.txt", 'a') as f:
        logging.info(f"{recording} launched")
        command = subprocess.Popen("exec " + command_str, stdin=subprocess.PIPE,
                                   stderr=f, shell=True)
        RUNNING_IDS[recording.id] = command
        command.termination_string = termination_string
        while command.poll() is None:
            time.sleep(0.5)
        logging.warning(f"{recording} exited")
        if recording.id in RUNNING_IDS:
            del RUNNING_IDS[recording.id]


def start_recording(recording: Recording):
    if len(recording.video_sources.all()) == 0:
        logging.error(f"Cannot start recording {recording.name}. No video sources available.")
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
    if not recording_method:
        logging.error(f"Cannot start recording {recording.name}. No recording method selected.")
        return
    name = recording.writing_directory + slugify(recording.name + " - " + recording.last_retry.strftime("%Y-%m-%d "
                                                                                                        "%H:%M:%S")) + ".mp4"
    command = format_str(recording_method.command, 'video_url', recording.selected_source.url)
    command = format_str(command, 'output_file_path', name)
    threading.Thread(target=launch_command, args=[command, recording, recording_method.termination_string]).start()
    recording.consecutive_retries += 1
    recording.total_retries += 1
    recording.save()


def stop_recording(recording: Recording):
    try:
        process: subprocess.Popen = RUNNING_IDS[recording.id]
        if recording.id in RUNNING_IDS:
            del RUNNING_IDS[recording.id]
        if process.termination_string:
            process.communicate(input=process.termination_string.encode("utf-8"))
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
        logging.info("Recordings check process started.")
        while True:
            current_date = datetime.datetime.now(tz=timezone.get_current_timezone())
            for recording in Recording.objects.exclude(id__in=RUNNING_IDS).filter(start_time__lte=current_date,
                                                                                  end_time__gt=current_date).prefetch_related(
                "video_sources", "video_sources__recording_method").select_related("selected_source__recording_method"):
                try:
                    start_recording(recording)
                except Exception as e:
                    logging.exception(f"{e}")
            for recording in Recording.objects.filter(id__in=RUNNING_IDS, end_time__lte=current_date):
                stop_recording(recording)
            time.sleep(1)
