import {Recording} from "./entities";

export function getStatus(rec: Partial<Recording>) {
    if(rec.start_time !== undefined) {
        if(rec.start_time > new Date()) {
            return "upcoming";
        }
        if(rec.start_time < new Date() && rec.end_time > new Date()) {
            return "running";
        }
        if(new Date() > rec.end_time) {
            return "passed";
        }
    }
    return "new"
}
