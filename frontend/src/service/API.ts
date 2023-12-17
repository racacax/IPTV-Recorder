import {M3UEntity, Recording, ShortPlaylist, Token, VideoSource} from "./entities"
import {types} from "sass";

export class API {
    public static API_ROOT = "/"
    public static CSRF_TOKEN = ""

    private static fetch(path: string, params = {}) {
        return fetch(API.API_ROOT + path, params)
    }
    private static fetchAuthenticated(path: string, params: any = {}) {
        if(params.headers === undefined) {
            params.headers = {}
        }
        params.headers["Authorization"] = "Token " + localStorage.getItem("iptvRecorderToken")
        params.headers["X-CSRFToken"] = API.CSRF_TOKEN
        return fetch(API.API_ROOT + path, params)
    }
    private static postOrPutAuthenticated(path: string, method: string, data: Object) {
        let params = {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }
        return API.fetchAuthenticated(path, params)
    }


    private static post(path: string, data: {}) {
        return fetch(API.API_ROOT + path, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, *cors, same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": API.CSRF_TOKEN
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: "follow", // manual, *follow, error
            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify(data), // le type utilisé pour le corps doit correspondre à })
        })
    }

    static getToken(username: string, password: string) {
        return API.post("api/token/", {"username": username, "password": password}).then(async r => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        }).then((j: Token) => {
            localStorage.setItem("iptvRecorderToken", j.token)
            return Promise.resolve()
        })
    }
    static check() {
        return API.fetchAuthenticated("api/check/").then(async r => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return Promise.resolve()
        })
    }
    static getRecordings() {
        return API.fetchAuthenticated("api/recordings/").then(async (r) : Promise<Recording[]> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        }).then((js) => {
            js.map(j => {
                j.start_time = new Date(j.start_time)
                j.end_time = new Date(j.end_time)
            })
            return Promise.resolve(js)
        })
    }


    static getPlaylists() {
        return API.fetchAuthenticated("api/playlists/").then(async (r) : Promise<ShortPlaylist[]> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }
    static getChannels(playlistId: number) {
        return API.fetchAuthenticated("api/playlists-m3u/" + playlistId + "/").then(async (r) : Promise<M3UEntity[]> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }
    static getRecording(id: number) {
        return API.fetchAuthenticated("api/recordings/" + id + "/").then(async (r) : Promise<Recording> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        }).then((j) => {
            j.start_time = new Date(j.start_time)
            j.end_time = new Date(j.end_time)
            return Promise.resolve(j)
        })
    }
    static createRecording(data: Partial<Recording>) {
        return API.postOrPutAuthenticated("api/recordings/", "POST", data).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }
    static updateRecording(id: number, data: Partial<Recording>) {
        return API.postOrPutAuthenticated("api/recordings/" + id + "/", "PUT", data).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }

    static deleteRecording(id: number) {
        return API.postOrPutAuthenticated("api/recordings/" + id + "/", "DELETE", {}).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return Promise.resolve()
        })
    }

    static createVideoSource(recordingId: number, data: Partial<VideoSource>) {
        return API.postOrPutAuthenticated("api/video-sources/" + recordingId + "/", "POST", data).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }
    static updateVideoSource(id: number, data: Partial<VideoSource>) {
        return API.postOrPutAuthenticated("api/video-source/" + id + "/", "PUT", data).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }
    static deleteVideoSource(id: number) {
        return API.postOrPutAuthenticated("api/video-source/" + id + "/", "DELETE", {}).then(async (r) : Promise<Object> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return Promise.resolve()
        })
    }
    static getVideoSourcesFromRecording(recordingId: number) {
        return API.fetchAuthenticated("api/video-sources/" + recordingId + "/").then(async (r) : Promise<VideoSource[]> => {
            if (r.status >= 300) {
                throw (await r.text())
            }
            return r.json()
        })
    }

}
