# IPTV Recorder
IPTV Recorder is a tool which allows to record streaming links like a PVR on a server. 
This tool provides:
- A server-side script which will manage your recordings (start, stop, retries)
- A web interface to schedule your recordings

Multiple playlists and accounts are supported. This tool was created with the aim to be able to record streams anywhere at anytime and be able to retrieve them easily on a distant server (via SSH/SFTP with Kodi or another mediacenter).

**/!\ DISCLAIMER: This tool does not provide any channel or any stream. You need to input your own M3U playlist to be able to use the software.**

## Installation
### Dockerfile
A docker image is provided along with the tool which allows you to install just by typing `docker-compose build` or `make update`. This image is shipped with `ffmpeg` and `wget` which are the two main recording methods available. To add custom commands, you'll need to either edit `Dockerfile` or use `make bash` to install other dependencies.

If you plan to run the software on Windows, you will most likely require to use it.
### Normal installation
#### Requirements
- Python (3.12 or higher)
- Makefile (required for make commands)
- ffmpeg and wget (not required but needed for quick installation)
#### Installation process
To install, just type `pip install -r requirements.txt` and all dependencies should be installed.
## Configuration
### .env
Create a .env file at root of project and fill it with
```dotenv
SECRET_KEY=Your Django secret key. Can be anything, see Django docs on how to generate one
ALLOWED_HOSTS=["localhost", "0.0.0.0"] // add any other host you may need
DEBUG=True // or False in production mode
RUNNING_PORT=8000 // or any other port
HOST=0.0.0.0
LANGUAGE_CODE=fr // or en for english
ENABLE_UWSGI=False // False if dev mode. Use True for production use !
```
For the next steps, we will consider you are not in production mode and UWSGI is not enabled (yet).
### Start project
Start project by typing `make up` (or `make up_d` if using Docker).
### User creation
You first need to create a superuser by typing command `make init` (or `make init_d` if using Docker).
### Command line vs Django Admin
IPTV Recorder is built with Django framework which provides an admin.

To set user data and playlist, you will need to set those information by following the next steps by either:
- Using some command lines
- Go to Django Admin (http://YOURHOST:PORT/admin/)

If using Docker, type `make bash` before doing next steps (command line only).
### User data definition
To set user data, type `python manage.py set_user_data`. The command prompt will ask you some information to fill (Recordings output directory, ...). You can also do it in Django admin by creating an "User data" object for your user.

### Add a playlist
To be able to use the software, you must have an M3U playlist (at least).

Type `python manage.py add_playlist` and fill information about it (name, URL, ...).

## Use the software
### Keep project in the background
For now, your project is running in your terminal. Close the program and either run `make up_detached` or `make up_detached_d` (if using Docker) to keep program open in background.
### Update
When updating program (via `git pull` or `git checkout`), you may need to restart program or run migrations with `make migrate` (or `make migrate_d`). You may also need to run a `pip install -r requirements.txt` before all of this (or `make update` if using Docker).
### Web page
The UI is running on the port you defined in `.env` file. So just go to http://YOURHOST:PORT .

## Keep project safe for production use
If your project is on a public server, security is important. Until now, you were using Django Dev Server which is not production ready.
To use your project in production, enable UWSGI in your `.env` file and configure a UWSGI proxy on the web server software you are using (Apache, NGINX, ...).
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
It has two parameters: {video_url}
  - {video_url} : Which will be replaced by the stream URL
  - {output_file_path} : Which will be replaced by the file destination

These two fields must be present in the command.