import { ref, Ref, watch } from "vue";
import {
  M3UEntity,
  Playlist,
  Recording,
  RecordingMethod,
  Token,
  VideoSource,
} from "./entities";

export type FetchReturn<T> = {
  error: Ref<string | null>;
  data: Ref<T | null>;
  loading: Ref<boolean>;
  fetchFn: (body?: object) => Promise<T>;
};

export type Options = {
  lazy?: boolean;
};
function fetchAndCatch<T>(
  url: Ref<string>,
  options: Options,
  method: "GET" | "PUT" | "POST" | "DELETE",
  formatFn: (t: unknown) => T,
): FetchReturn<T> {
  const error: Ref<string | null> = ref(null);
  const data: Ref<T | null> = ref(null);
  const loading: Ref<boolean> = ref(false);
  const fetchFn = (body?: object) => {
    error.value = null;
    loading.value = true;
    data.value = null;
    const result =
      method === "GET"
        ? API.fetchAuthenticated(url.value)
        : API.postOrPutAuthenticated(url.value, method, body);
    return result
      .then((r) => {
        if (r.status >= 400) {
          if (r.status == 403) {
            error.value =
              "Got error :403 Forbidden. Might be rate limited (slow down your clicks bucko).";
            return null;
          } else {
            return r
              .json()
              .then((j) => {
                error.value = j?.message ?? "Unknown error";
                return null;
              })
              .catch(() => {
                error.value = "Unknown error";
                return null;
              });
          }
        }
        return r.json();
      })
      .catch((e) => {
        error.value = e.toString();
        loading.value = false;
      })
      .then((v) => {
        if (formatFn) {
          if (Object.prototype.toString.call(v) === "[object Array]") {
            data.value = v.map(formatFn);
          } else {
            data.value = formatFn(v);
          }
        } else {
          data.value = v;
        }
        loading.value = false;
        return data.value;
      });
  };
  if (!options.lazy) {
    watch([url], fetchFn);
    fetchFn();
  }

  return { error, data, loading, fetchFn };
}

function urlManager<T>(
  getUrl: () => string,
  refs: Ref<unknown>[] | (() => Record<string, unknown>) | (() => unknown),
  options: Options,
  method: "GET" | "PUT" | "POST" | "DELETE",
  formatFn?: (t: unknown) => T,
): FetchReturn<T> {
  const url = ref<string>(getUrl());
  watch(refs, () => {
    url.value = getUrl();
  });
  return fetchAndCatch(url, options, method, formatFn);
}

export class API<T> {
  private readonly endpoint: string;
  public static API_ROOT = "/";
  public static CSRF_TOKEN = "";
  private readonly formatFn: (t: unknown) => T;

  constructor(endpoint: string, formatFn?: (t: unknown) => T) {
    this.endpoint = endpoint;
    this.formatFn = formatFn;
  }
  public static fetchAuthenticated(path: string, params?: RequestInit) {
    if(!params) params = {}
    if (params.headers === undefined) {
      params.headers = {};
    }
    params.headers["Authorization"] =
      "Token " + localStorage.getItem("iptvRecorderToken");
    params.headers["X-CSRFToken"] = API.CSRF_TOKEN;
    return fetch(API.API_ROOT + path, params);
  }

  public static postOrPutAuthenticated(
    path: string,
    method: string,
    data: object,
  ) {
    const params = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    return API.fetchAuthenticated(path, params);
  }

  private static post(path: string, data: object) {
    return fetch(API.API_ROOT + path, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": API.CSRF_TOKEN,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data), // le type utilisé pour le corps doit correspondre à })
    });
  }

  static getToken(username: string, password: string) {
    return API.post("api/token/", { username: username, password: password })
      .then(async (r) => {
        if (r.status >= 300) {
          throw await r.text();
        }
        return r.json();
      })
      .then((j: Token) => {
        localStorage.setItem("iptvRecorderToken", j.token);
        return Promise.resolve();
      });
  }

  get(getVariables: () => number, options: Options = {}): FetchReturn<T> {
    const getUrl = () => {
      return `${this.endpoint}${getVariables()}/`;
    };
    return urlManager(getUrl, getVariables, options, "GET", this.formatFn);
  }
  list(options: Options = {}): FetchReturn<T[]> {
    const getUrl = () => {
      return this.endpoint;
    };
    return urlManager(getUrl, [], options, "GET", this.formatFn) as FetchReturn<
      T[]
    >;
  }
  post(options: Options = {}): FetchReturn<{ created: boolean; id: number }> {
    const getUrl = () => {
      return this.endpoint;
    };
    return urlManager(getUrl, [], options, "POST");
  }

  put(getVariables: () => number, options: Options = {}): FetchReturn<T> {
    const getUrl = () => {
      return `${this.endpoint}${getVariables()}/`;
    };
    return urlManager(getUrl, getVariables, options, "PUT");
  }

  delete(getVariables: () => number, options: Options = {}): FetchReturn<T> {
    const getUrl = () => {
      return `${this.endpoint}${getVariables()}/`;
    };
    return urlManager(getUrl, getVariables, options, "DELETE");
  }
}

export const CheckClient = new API("api/check/");
export const RecordingClient = new API<Recording>(
  "api/recordings/",
  (e: Recording) => ({
    ...e,
    start_time: new Date(e.start_time),
    end_time: new Date(e.end_time),
  }),
);
export const RecordingMethodClient = new API<RecordingMethod>(
  "api/recording-methods/",
);
export const PlaylistM3UClient = new API<M3UEntity[]>("api/playlists-m3u/");
export const PlaylistClient = new API<Playlist>("api/playlists/");
export const VideoSourcesClient = new API<VideoSource>("api/video-sources/");
export const VideoSourceClient = new API<VideoSource>("api/video-source/");
