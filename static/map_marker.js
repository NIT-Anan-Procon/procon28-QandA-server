var interviews = new Array();
var interviewmessages = new Array();

function latlng2list(latlng){
    var latlng_list = latlng.split("/");
    var lat = Number(latlng_list[0]);
    var lng = Number(latlng_list[1]);
    return [lat, lng];
}

function add_marker(patient_id, state, latlng, records, cares, require_encode){
    var icon = "";
    switch (state){
        case 1:
            icon = 'leaflet-marker-icon-color-blue';
            break;
        case 2:
            icon = 'leaflet-marker-icon-color-yellow';
            break;
        case 3:
            icon = 'leaflet-marker-icon-color-red';
            break;
    }

    var records_ = new Array();

    //encode is required when records is sent via socketio
    if(require_encode){
        for(var i = 0; i < records.length; i++){
            var record = records[i];
            var text = "";
            for(var j = 0; j < record.length; j++){
                text += String(record[j]);
            }
            if (i == records.length-1){
                break;
            } else {

            }

            records_.push(text);
        }
    } else {
        records_ = records.split(":");
    }

    var marker = L.marker(
        latlng2list(latlng),
        { title: "marker-title" }
    )
    .addTo(map)
    .on("click", function(){
        $("#table_id").text(String(patient_id));
        $("#table_latlng").text(String(latlng));
        $("#table_state").text(String(state));

        var ul = document.getElementById("table_cares_list");
        $("#table_cares_list").empty('');
        
        cares_list = cares.split(":");
        for (i = 0; i < cares_list.length; i++){
            var care = cares_list[i];
            var li = document.createElement('li');
            li.appendChild(document.createTextNode(care));
            ul.appendChild(li);
        }

        var ul = document.getElementById("table_records_list");
        $("#table_records_list").empty('');

        for (i = 0; i < records_.length; i++){
            var record = records_[i]
            var li = document.createElement('li');
            li.appendChild(document.createTextNode(record));
            ul.appendChild(li);
        }

    });
    L.DomUtil.addClass( marker._icon, icon );

    interviews[patient_id] = marker
    interviewmessages[patient_id] = {"patient_id":patient_id, "state":state, "latlng":latlng, "records":text};

}

function delete_marker(msg){
    var marker = interviews[msg.patient_id]
    map.removeLayer(marker);
};