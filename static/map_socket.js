
namespace = "/map"
var socket = io.connect('//' + document.domain + ':' + location.port + namespace);

socket.on('add new marker', function(msg) {
    add_marker(
        msg.patient_id,
        msg.state,
        msg.latlng,
        msg.interview_records,
        msg.cares,
        msg.address,
        true
    )
});

socket.on('delete a marker', function(msg) {
    delete_marker(msg)
});

socket.on('change the state', function(new_msg) {
    delete_marker(new_msg)
    msg = interviewmessages[new_msg.patient_id]
    add_marker(
        msg.patient_id,
        new_msg.state,
        msg.latlng,
        new_msg.records,
        new_msg.cares,
        new_msg.address,
        false
    )
});

socket.on('delete all markers', function(msgs){
    for(var i = 0; i < msgs.patient_ids.length; i++){
        var msg = msgs.patient_ids[i];
        delete_marker(msg)
    }
});


function send_recommend_cares(patient_id, care_indices){
    socket.emit('recommend care', {id: patient_id, care:care_indices});
}
