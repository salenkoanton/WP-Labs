function songSearchTemplate(songs){
    return Mustache.to_html('{{#data}}<div class="post addAudioPost"><h4 style="display: inline-block;"><a href="/author/{{author.id}}">{{author.name}}</a> - {{name}}</h4><button class="btn pull-right addAudioInInput" type="submit" value="{{id}}">+</button><hr></div>{{/data}}{{^data}}<div class="post addAudioPost"><h4 style="display: inline-block;">We can`t find your audios</h4></div>{{/data}}', {data: songs});
}

function showComments(id) {
            x = document.getElementById(id);
            if(x.hasAttribute("hidden")){
                  x.removeAttribute("hidden");
                }
            else{
            x.setAttribute("hidden", true);}
        };
$(document).ready(function(){
$("#delete-post").click(function(){
    btn = $(this);
    $.ajax({type: "delete", url: $(location).attr('pathname') + '/' + btn.attr("value"), success: function(result){
        let res = jQuery.parseJSON(result);
        if (res.status === 'error'){
            alert('error');}
        else
            {$("#post_" + btn.attr("value")).remove();}
    }});

});
});
$(document).ready(function(){
$(".deletePost").click(function(){
    btn = $(this);
    inp = $("#delete-post");
    inp.attr("value", btn.attr("value"));
});
});

$(document).ready(function(){
    $("#searchAddButton").click(function(){
        btn = $(this);
        inp = $("#searchAdd");
        $.ajax({type: "GET", data: {search: inp.val(), xhr: true}, success: function(result){
            let audios = jQuery.parseJSON(result);
            $(".addAudioPost").remove();
            $("#addAudioModal").prepend(songSearchTemplate(audios));

            audioBtnEvent();
        }});
    });
});
function audioBtnEvent(){
    $(document).ready(function(){
        $(".addAudioInInput").click(function(){
            addAudioInInput($(this).val(), 'addAudioInp');
             if(this.innerHTML == '+'){
                this.innerHTML = '&times;';
             }
             else {
                this.innerHTML = '+';
             }
        });
    });
 };
audioBtnEvent();