export interface Token {
  token: string;
}
export interface ShortPlaylist {
  id: number;
  name: string;
}
export interface Playlist extends ShortPlaylist {
  url: string;
  epg_url: string;
  last_updated: Date;
  refresh_gap: number;
}
export interface VideoSource {
  id: number;
  url: string;
  name: string;
  logo: string | null;
  recording_method_id: number;
  index: number;
}
export interface FVideoSource extends VideoSource {
  action: string;
}
export interface Recording {
  id: number;
  writing_directory: string;
  start_time: Date;
  end_time: Date;
  name: string;
  gap_between_retries: number;
  use_backup_after: number;
  last_retry: Date;
  consecutive_retries: number;
  total_retries: number;
  is_running: boolean;
  default_source: VideoSource;
}

export interface FRecording extends Recording {
  action: string;
}

export interface M3UEntity {
  name: string;
  logo: string;
  url: string;
  category: string;
  tvg: Tvg;
}
export interface Tvg {
  id: string;
  name: string;
  url: null;
}

export interface RecordingMethod {
  id: number;
  name: string;
  command: string;
  termination_string: string;
}
