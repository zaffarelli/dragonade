class Main{
    constructor(){
    }

    prepareAjax() {
        let me = this;
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    let csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                    xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
                }
            }
        });
    }

    revealUI(){
        let me=this;
        console.log("Reveal UI");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.universe').addClass('hidden');
        $('.universe').removeClass('shown');
        $('.sheet').addClass('hidden');
    }

    revealUniverse(){
        let me=this;
        console.log("Reveal Universe");
        $('.world').removeClass('shownflex');
        $('.universe').removeClass('hidden');

        $('.world').addClass('hidden');
        $('.universe').addClass('shown');

    }

    perform(){
        let me = this;
        me.prepareAjax();
        me.registerActions();
    }

    registerActions(){
        let me = this;
        me.registerEditables();
        me.registerSheets();
    }

    registerEditables(){
        let me = this;
        $('.editable').off().on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            let action = $(this).attr('action');
            let id = $(this).attr('id');
            let change = ''
            console.log(action);
            console.log(id);
            if (action == "inc_dec"){
                let params = id.split("__");
                if (params.length > 2){
                    if (e.ctrlKey){
                        change = 'plus';
                        console.log("Ctrl key")

                    }
                    else if (e.shiftKey){
                        change = 'minus'
                        console.log("Shift key");
                    }
                    let data = params[0]+"__"+params[1]+"__"+params[2]+"__"+change;
                    if (change != ''){
                        $.ajax({
                            url: 'ajax/inc_dec',
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data: {
                                params: data,
                            },
                            dataType: 'json',
                            success: function (answer) {
                                $('#roster_'+answer.id).html(answer.new_roster);
                                me.registerActions();
                            },
                            error: function (answer) {
                                console.error('Error... ' + answer);
                            },
                        });
                    }

                }else{
                    console.log("Wrong parameters number...")
                }
            }else{
                console.log("Unknown action...")
            }
        });
    }

    registerSheets(){
        let me = this;
        $('.minisheet').off().on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let words = miniid.split('_');
            let id = words[0];
            $('.sheet.base').addClass('hidden');
            $('.sheet.skills').addClass('hidden');
            $('.minisheet').removeClass('mark');
            $(this).addClass('mark');
            $("#sss_"+id).removeClass('hidden');
            $("#ssm_"+id).removeClass('hidden');
            $("#ssg_"+id).removeClass('hidden');
            $("#ssp_"+id).removeClass('hidden');
            $("#ssc_"+id).removeClass('hidden');
            $("#ssd_"+id).removeClass('hidden');
            $("#sb_"+id).removeClass('hidden');
            me.registerActions();
        });
    }

}