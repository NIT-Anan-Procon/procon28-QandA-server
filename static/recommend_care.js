var care_select = document.getElementById('listbox_recommend_care');
var selected = new Array();
var s_o = care_select.options;

var last_indices = new Array();

function findVal(value){
    for (var i = 0; i < last_indices.length; i++){
        if (last_indices[i] == value){
            return i;
        }
    }
    return -1;
}

$(function($){

    $("#listbox_recommend_care").change(function(){
        console.log($(this).val());


        selected_num = 0

        console.log(selected_num)

        var index = $(this).val()[0];
        console.log(index)
        valueIndex = findVal(index);
        console.log(valueIndex)
        if (valueIndex === -1){ //not selected in the last state
            s_o[index].selected=true;

            for(var i = 0; i < last_indices.length; i++){
                console.log(s_o[last_indices[i]])
                s_o[last_indices[i]].selected = true;
            } 
        } else {

            for(var i = 0; i < last_indices.length; i++){
                s_o[last_indices[i]].selected = true;
            } 
            s_o[last_indices[valueIndex]].selected = false;
        }
    });

    $("#listbox_recommend_care").click(function(){
        if (last_indices.length == $(this).val().length){
            s_o[last_indices[0]].selected = false;
        }
        last_indices = $(this).val();
        console.log(last_indices)
    });
});

function select_care(){
}