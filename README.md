# IPTV Recorder
IPTV Recorder is a tool which allows to record streaming links like a PVR on a server. 
This tool provides:
- A server-side script which will manage your recordings (start, stop, retries)
- A web interface to schedule your recordings

![preview](https://i.imgur.com/xM6DDKN.png)
Multiple playlists and accounts are supported. This tool was created with the aim to be able to record streams anywhere at anytime and be able to retrieve them easily on a distant server (via SSH/SFTP with Kodi or another mediacenter).

**/!\ DISCLAIMER: This tool does not provide any channel or any stream. You need to input your own M3U playlist to be able to use the software.**

## Installation
### Dockerfile
A docker image is provided along with the tool which allows you to install just by typing `docker-compose build` or `make update`. This image is shipped with `ffmpeg` and `wget` which are the two main recording methods available. To add custom commands, you'll need to either edit `Dockerfile` or use `make bash` to install other dependencies.

**If you use Docker, the output port will be 35699. However, you must keep 8000 as a port in the configuration.**

If you plan to run the software on Windows, you will most likely require to use it.


**For any following make command, if you use Docker, you must add `_d` at the end (e.g. `make up` becomes `make up_d`). Another solution is to run make commands inside Docker bash (this works for every command except `make up`).**

**For any python command (e.g `python manage.py set_user_data`), if you use Docker, you must be inside Docker container bash to run it.**

**To enter Docker container bash, type `make bash`.**

### Normal installation
#### Requirements
- Python (3.12 or higher)
- Makefile (required for make commands)
- ffmpeg and wget (not required but needed for quick installation)
#### Installation process
To install, just type `pip install -r requirements-dev.txt` and all dependencies should be installed.

Note: You may need to create a virtual-env depending on your Python configuration (and it is recommended to do so).
## Configuration
### Start project
Start project by typing `make up` or `make up_d` (if using Docker). You should see the database being created. An error message stating `CommandError: You must set settings.ALLOWED_HOSTS if DEBUG is False.` should appear. This is normal, our .env isn't configurated yet. You shouldn't have any other error. 
### Init script
Type `make init`. This will trigger .env definition process and necessary steps.
#### .env
Basic information will be set in the definition of .env file. The most important part is `ALLOWED_HOSTS` step. You must add the host where you will access your app.

**DEBUG mode and uWSGI will be disabled. But it is recommended to disable DEBUG and enable uWSGI once all is configured (see one of the later points).**
#### User creation
This will create a super user which will be able to access the whole admin of the app. You'll also set the recordings writing directory path.

If you want to add another user in the future, just head to Django admin and once user is created, type command `python manage.py set_user_data`.
#### Add playlist
You must set a playlist for the user to be able to use the software. Playlist has to be in M3U format.

**Note: The software struggles with large files for now. Try to provide a filtered playlist.**

If you want to add another playlist in the future, either head to Django Admin. Or type command `python manage.py add_playlist`.
#### Restart program
Once everything is setup close the program and restart it. You should see it running at address http://YOURHOST:PORT/
## Use the software
### Keep project in the background
For now, your project is running in your terminal. Close the program and either run `make up_detached` or `make up_detached_d` (if using Docker) to keep program open in background.
### Update
When updating program (via `git pull` or `git checkout`), you may need to restart program or run migrations with `make migrate` (or `make migrate_d`). You may also need to run a `pip install -r requirements.txt` before all of this (or `make update` if using Docker).
### Web page
The UI is running on the port you defined in `.env` file. So just go to http://YOURHOST:PORT .

## Keep project safe for production use
If your project is on a public server, security is important. Until now, you were using Django Dev Server which is not production ready.
To use your project in production:
- Install uWSGI by typing (if not using Docker. Docker image already has it preinstalled.)
```pip install -r requirements.txt```
- Enable UWSGI in your `.env` file and configure a UWSGI proxy on the web server software you are using (Apache, NGINX, ...).
There are mods to be able to do that:
- https://httpd.apache.org/docs/2.4/fr/mod/mod_proxy_uwsgi.html
- https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html

## Add/edit custom commands
By default, two commands are set :
- ffmpeg: Takes any stream and outputs it to an MP4 file without transcoding.
- wget: Downloads raw video into an MP4 file. Only supports unsegmented streams.

You may want to customize them or add other programs. All you need to do is head to Django admin and connect with a superuser. 

Then go to `Recording methods` and either add or edit entries.
- Termination string can be omitted. By default it is "q" for ffmpeg. Sending q to ffmpeg triggers the end of the program and lets the encoding process finish properly (to avoid corrupted file). This may differ depending on programs (wget doesn't have one for instance).
- command field contains the command that will be triggered. 
It has two parameters:
  - {video_url} : Which will be replaced by the stream URL
  - {output_file_path} : Which will be replaced by the file destination

These two fields must be present in the command.