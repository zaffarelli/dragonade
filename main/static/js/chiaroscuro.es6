const ZAFF_MATCHES = [['é', 'WeA_'], ['é', 'WeG_'], ['à', 'WeG_'], ['ï', 'WiT_'], ['ë', 'WeT_'], ['ä', 'WaT_'],
    ['ù', 'WuG_'],['ç', 'WcC_'], ['ô', 'WoC_'], ['ê', 'WeC_'], ['â', 'WaC_'], [' ', 'Wsp_'], ["'", 'Wsq_'], ['"', 'Wdq_']]

class Chiaroscuro {
    constructor(config) {
        this.config = config;
        this.name = "Chiaroscuro";
        this.modules = []
        this.globalPerformers = []
        this.axiomaticPerformers = []
        if (config["modules"].includes("orologio") == true) {
            let mod = new Orologio(this, config);
            mod.register();
        }
        if (config["modules"].includes("carte") == true) {
            let mod = new Carte(this, config);
            mod.register();
        }
        if (config["modules"].includes("risorse") == true) {
            let mod = new Risorse(this, config);
            mod.register();
        }
        if (config["modules"].includes("piani") == true) {
            let mod = new Piani(this, config);
            mod.register();
        }
        this.tables = []
    }

    prepareWebSocket(){
        let me = this;
        $("#parallax_reveal").off().on('submit', (e) => {
            e.preventDefault();
            let message = e.target.message.value
            me.chatSocket.send(JSON.stringify({
                'type':'reveal',
                'message':message
            }))
            return false;
        })
        $("#parallax_select").off().on('submit', (e) => {
            e.preventDefault();
            let message = e.target.message.value
            let message_type = e.target.message.value
            me.chatSocket.send(JSON.stringify({
                'type':'select',
                'message':message
            }))
            return false;
        })
    }

    softLog(name, txt) {
        let me = this;
        if (name == "") {
            name = me.name;
        }
        let str = "[" + name + "] > " + txt;
        console.debug(str);
    }

    hardLog(name, txt) {
        let me = this;
        if (name == "") {
            name = me.name;
        }
        let str = "[" + name + "] > " + txt;
        console.log(str);
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

    revealUI() {
        let me = this;
        console.log("Reveal UI");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.universe').addClass('hidden');
        $('.universe').removeClass('shown');
        $('.sheet').addClass('hidden');
    }

    revealUniverse() {
        let me = this;
        console.log("Reveal Universe");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.universe').removeClass('hidden');

        //$('.world').addClass('hidden');
        //$('.universe').addClass('shown');

    }


    registerActions() {
        let me = this;
        me.registerEditables();
        me.registerValuePush();
        me.registerSheets();
        me.registerLinks();
        me.registerMiniItems();
        me.registerShowHide();
        me.registerPaginator();
    }

    registerEditables() {
        let me = this;
        $('.btn_edit').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let action = $(this).attr('action');
            let id = $(this).attr('id');
            let change = ''
            if (action == "inc_dec") {
                let params = id.split("__");
                if (params.length > 3) {
                    //if (e.ctrlKey) {
                        change = params[3];
                    //}
                    let data = params[0] + "__" + params[1] + "__" + params[2] + "__" + change;
                    if (change != '') {
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
                                $('#roster_' + answer.id).html(answer.new_roster);
                                $(".for_display_" + answer.id).addClass('hidden');
                                $(".for_edit_" + answer.id).removeClass('hidden');
                                me.registerActions();
                            },
                            error: function (answer) {
                                console.error('Error... ' + answer);
                            },
                        });
                    }

                } else {
                    console.log("Wrong parameters number...")
                }
            } else if (action == "value") {
                let params = id.split("__");
                let value = $(this).attr("srcval");

                let pvalue = me.zaff_decode(value)

                //let pvalue = window.atob(bvalue);
//                  let cvalue = pvalue.replace(/[\u00A0-\u9999<>\&]/g, function(i) {
//                      return '&#'+i.charCodeAt(0)+';';
//                  });
                //let value = he.unescape(pvalue,{'strict':true})
                //console.log("bvalue:",bvalue)
                console.log("value:",value)
//                 console.log("cvalue:",cvalue)
                //console.log("value: ",value)
                if (params.length > 3) {
                    if (e.ctrlKey) {
                        change = params[3];
                    }
                    let data = params[0] + "__" + params[1] + "__" + params[2] + "__" + change;
                    $("#target_ed").val(data);
                    $("#ed").val(pvalue);
                    $("#echo").html(value);
                    me.registerActions();
                } else {
                    console.log("Wrong parameters number...")
                }
            } else {
                console.log("Unknown action...")
            }
        });
    }

    registerValuePush() {
        let me = this;
        $('#valuepush_ed').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let new_value = $('#ed').val()
            console.log(new_value)
            let value = me.zaff_encode(new_value)
            console.log("zvalue",value)
            let refs = $("#target_ed").val();


            $.ajax({
                url: 'ajax/value_push',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {
                    "new_value": value,
                    "refs": refs
                },
                dataType: 'json',
                success: function (answer) {
                    $('#roster_' + answer.id).html(answer.new_roster);
                    $(".for_display_" + answer.id).addClass('hidden');
                    $(".for_edit_" + answer.id).removeClass('hidden');
                    $("#target_ed").val("");
                    $("#ed").val("");
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ' + answer);
                },
            });
        });
    }

    registerPaginator() {
        let me = this;
        $('.paginator').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            console.log("paginator")
            let page = $(this).attr("page")
            $.ajax({
                url: 'ajax/paginator',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {
                    "page": page
                },
                dataType: 'json',
                success: function (answer) {
                    $('.list').html(answer.html);
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ' + answer);
                },
            });
        });
    }


    registerSheets() {
        let me = this;
        $('.minisheet').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let words = miniid.split('__');
            let id = words[1];
            $('.roster .sheet').addClass('hidden');
            //$('.sheet.skills').addClass('hidden');
            $('.minisheet').removeClass('mark');
            $(this).addClass('mark');
            $(".roster").addClass('hidden');
            $("#roster_" + id).removeClass('hidden');
            $("#roster_" + id + " .sheet").removeClass('hidden');
            console.log("#roster_" + id + ".sheet")
            //$("#sb_"+id).removeClass('hidden');
            $(".for_display_" + id).removeClass('hidden');
            $(".for_edit_" + id).addClass('hidden');
            me.registerActions();
        });
        $('.skill_switch').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let words = miniid.split('_');
            let id = words[0];
            $(".roster").addClass('hidden');
            $("#roster_" + id).removeClass('hidden');
            $(".for_display_" + id).toggleClass('hidden');
            $(".for_edit_" + id).toggleClass('hidden');
            me.registerActions();
        });
    }


    registerMiniItems() {
        let me = this;
        $('.mini').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let code = $(this).attr('code');
            let words = miniid.split('__');
            let id = words[1];
            console.log("mini item click!")
            $(".item").addClass('hidden');
            $(".mini").removeClass('mark');
            $("#mini__" + id).addClass('mark');
            $("#item__" + id).removeClass('hidden');
            $(".for_display_" + id).removeClass('hidden');
            $(".for_edit_" + id).addClass('hidden');
            me.axiomaticPerformers.forEach( (m) => {
                console.log(`Sending code ${code} to axiomatic performer [${m.name}].`)
                m.perform(code)
            });

            //me.pa.perform("#item__" + id, code);
            me.registerActions();
        });

    }

    registerLinks() {
        let me = this;
        $('.link').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let link_to = $(this).attr('link_to');
            if (link_to != "") {
                window.location = link_to;
            }
        });
    }

    registerShowHide() {
        let me = this;
        $('.showhide').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let tgt = $(this).attr("target");
            if ($(this).hasClass("times")){
                $("."+tgt).addClass("hidden");
                $(".showhide.eye").removeClass("hidden");
                $(".corpus").css("right","0");
                me.resizeEvent();
            }else if ($(this).hasClass("eye")){
                $("."+tgt).removeClass("hidden");
                $(".showhide.eye").addClass("hidden");
                $(".corpus").css("right","30vw");
                me.resizeEvent();
            }
        });
    }

    resizeEvent(){
        let me= this;
        _.forEach(me.modules,
                (m) => {
                    m.resizeEvent();
                }
            );
    }

    dispatchMessage(type,message){
        let me = this;
        _.forEach(me.globalPerformers,
            (m) => {
                m.action(type,message);
            }
        );

    }

    perform() {
        let me = this;
        let no_global = true
        let url = `ws://192.168.0.25:8083/ws/socket-server/`;
        me.chatSocket = new WebSocket(url)
        me.chatSocket.onmessage = function(e){
            let data = JSON.parse(e.data)
            console.log("Data:",data)
            if (data.type === "select"){
                $("#info").prepend(
                `<div>
                    <p>${data.message}</p>
                </div>`
                )
                me.dispatchMessage(data.type,data.message);
            }else{
                me.dispatchMessage(data.type,data.message);
            }
        }
        me.prepareAjax();
        me.registerActions();
        //window.addEventListener('resize',resizeEvent);
        console.log("Global Perform");
        _.forEach(me.globalPerformers,
            (m) => {
                m.perform();
                no_global = false;
            }
        );
        if (no_global){
            me.revealUI();
        }
        me.prepareWebSocket()
        //me.resizeEvent();
    }

    zaff_encode(str){
        let zstr = str
        _.forEach(ZAFF_MATCHES, (m) => {
            zstr = zstr.replaceAll(m[0], m[1])
        })
        return zstr
    }

    zaff_decode(zstr){
        let str = zstr
        _.forEach(ZAFF_MATCHES, (m) => {
            str = str.replaceAll(m[1], m[0])
        })
        return str
    }




}