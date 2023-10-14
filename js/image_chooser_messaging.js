import { api } from "../../../scripts/api.js";

function send_message_from_pausing_node(message) {
    const id = app.graph._nodes_by_id[app.runningNodeId.toString()].widgets[0].value;
    send_message(id, message);
}

function send_message(id, message) {
    const body = new FormData();
    body.append('message',message);
    body.append('id', id);
    api.fetchApi("/image_chooser_message", { method: "POST", body, });
}

function send_cancel() {
    send_message(-1,'__cancel__');
    api.interrupt();
}

var skip_next = 0;
function skip_next_restart_message() { skip_next += 1; }
function send_onstart() {
    if (skip_next>0) {
        skip_next -= 1;
    } else {
        send_message(-1,'__start__');
    }
}

export { send_message_from_pausing_node, send_cancel, send_message, send_onstart, skip_next_restart_message }
