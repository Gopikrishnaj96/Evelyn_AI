let siriWave = null; // Declare globally

$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sync:true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect:"bounceOut",

        },
    });
    //Siri config
    
    // Initialize SiriWave only once
    if (!siriWave) {
        siriWave = new SiriWave({
            container: document.getElementById("siri-container"),
            width: 810,
            height: 250,
            style: "ios9",
            speed: 0.3,
            amplitude: "1",
            autostart: true
        });
    }

    //siri msg animation
    $('.siri-message').textillate({
        loop: false,
        sync:true,
        minDisplayTime: 1000,
        in:{
            effect: "fadeInUp",
            sync:true
        },
        out:{
            effect:"fadeOutUp",
            sync:true,
        },
    });
    $("#MicBtn").click(function () { 
        //eel.playAssistandSound()
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false)
        eel.allCommands()()
    });

    function doc_keyUp(e){
        //check for ctrl  key +40(down arrow)
        if ((e.ctrlKey && e.key.toLowerCase() === 'e')) {
            //eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup',doc_keyUp,false);

    function PlayAssistant(message){

        if(message!="")
        {
            $("#Oval").attr("hidden",true);
            $("#SiriWave").attr("hidden",false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden',true)
        }
    }
    function ShowHideButton(message){
        if(message.length==0){
            $("#MicBtn").attr('hidden',false);
            $("#SendBtn").attr('hidden',true);
        }
        else{
            $("#MicBtn").attr('hidden',true);
            $("#SendBtn").attr('hidden',false);
        }
    }
    $("#chatbox").keyup(function(){
        let message = $("#chatbox").val();
        ShowHideButton(message)
    });
    $("#SendBtn").click(function(){
        let  message=$("#chatbox").val()
        PlayAssistant(message)
    });

    $("#chatbox").keypress(function(e){
        key=e.which;
        if(key==13){
            let message=$("#chatbox").val()
            PlayAssistant(message)
        }
    });
    
    window.onbeforeunload = () => {
        eel.on_close();
    };
});