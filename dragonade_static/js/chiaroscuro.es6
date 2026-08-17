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
        if (config["modules"].includes("appartuses") == true) {
            let mod = new Appartus(this, config);
            mod.register();
        }
        if (config["modules"].includes("stregoneria") == true) {
            let mod = new Stregoneria(this, config);
            mod.register();
        }
        if (config["modules"].includes("combattimento") == true) {
            let mod = new Combattimento(this, config);
            mod.register();
        }
        this.tables = []
        this.last_tabbutton = ""
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
//          console.log(str);
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
//         console.log("Reveal UI");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
//         $('.universe').addClass('hidden');
//         $('.universe').removeClass('shown');
        $('.sheet').addClass('hidden');
    }

    revealUniverse() {
        let me = this;
//         console.log("Reveal Universe");
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
//         $('.universe').addClass('shownflex');
        $('.universe').removeClass('hidden');

        //$('.world').addClass('hidden');
        //$('.universe').addClass('shown');

    }


    registerActions() {
        let me = this;
        me.prepareAjax()
        me.registerShortcuts()
        me.registerEditables()
        me.registerStackPull()
        me.registerValuePush()
        me.registerSheets()
        me.registerLinks()
        me.registerMiniItems()
        me.registerShowHide()
        me.registerPaginator()
        me.registerModelForm()
        me.registerShifters()
        me.registerTabs()
        me.registerListActions()

    }

    registerShortcuts(){
        let me=this
        $("body").off().on("keyup", (e) => {
            e.preventDefault()
            e.stopPropagation()
            if (e.ctrlKey && e.altKey){
                switch (e.key) {
                    case "o":
                        console.log("Code:"+e.code, "Key:"+e.key)
                        $("#options_showhide").trigger('click')
                        break
                }
            }

        })
    }

    registerTabs() {
        let me = this;
        $('.tabbutton').off().on('click', function (e) {
            let tgt = $(this).attr("param")
            $(".tabbutton").removeClass("on")
            $("#tabbutton_"+tgt).addClass("on")
            $(".tabpanel").addClass("hidden")
            $("#tabpanel_"+tgt).removeClass("hidden")
            me.last_tabbutton = $(this).attr("id")
            console.log(`Last tab button is [${me.last_tabbutton}].`)
        })
    }


    registerStackPull() {
        let me = this;
        $('.stackpull').off().on('click', function (e) {
            let html = $(this).attr('param')
            let action = $(this).attr('action')
            $("#ed").val(html)
            $("#target_ed").val(action);
        })
        $('.stackpush').off().on('click', function (e) {
            console.log("stackpush")
            let list = $("#ed").val()
            let words = list.split(" ")
            let word = $(this).attr('param')
            if (!words.includes(word)){
                words.push(word)
            }
            let html = words.join(" ")
            $("#ed").val(html)
        })
    }

    registerListActions(){
        let me = this
        $('.list_action').off().on('click', function(e) {
            let id = $(this).attr('id')
            let words = id.split('__')
            let rid = words[0]
            let action = words[1]
            switch (action){
                case "view":
                    console.log(`Viewing for [${rid}] required.`)
                    me.axiomaticPerformers.forEach( (m) => {
                        console.log(`[${m.name}] is ready to handle [${rid}]!`)
                        m.handle(rid)
                    })
                    me.registerActions()
                    break
                case "edit":
                    console.log(`Editing for [${words[0]}] required.`)
                    break
                case "export":
                    console.log(`Exporting for [${words[0]}] required.`)
                    break
                default:
                    console.warn(`Unknown list action [${words[1]}] for item [${words[0]}].`)
                    break
            }
        })
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
//                                 $('#roster_' + answer.id).html(answer.new_roster);
//                                 $(".for_display_" + answer.id).addClass('hidden');
//                                 $(".for_edit_" + answer.id).removeClass('hidden');
                                $('#roster_' + answer.id).remove()
                                //$div = $('<div>',{id:'roster_'+answer.id,class:"roster"})
                                $('.container').append(answer.new_roster);
                                console.log(answer.new_roster)
                                $('#roster_' + answer.id).removeClass("hidden")
                                $(".for_display_" + answer.id).addClass('hidden');
                                $(".for_edit_" + answer.id).removeClass('hidden');
//                                 $("#target_ed").val("");
//                                 $("#ed").val("");
                                me.registerActions();
                                if (me.last_tabbutton != ""){
                                    console.log(`${me.last_tabbutton}`)
                                    $("#"+me.last_tabbutton).trigger("click")
                                }
                            },
                            error: function (answer) {
                                console.error('Error... ' + answer);
                            },
                        });
                    }

                } else {
                    console.error("Wrong parameters number...")
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
//                 console.log("value:",value)
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
                    console.error("Wrong parameters number...")
                }
            } else {
                console.warning("Unknown action...")
            }
        });
    }

    registerShifters(){
        let me = this
        $('.shifter').off().on('click', function(e){
            e.preventDefault()
            e.stopPropagation()
            let miniid = $(this).attr('id')
            let words = miniid.split('__')
            let model = $(this).attr('model')
            // console.log(`rid:${words[0]} param:${words[1]}`)
            if (e.ctrlKey || e.altKey) {
                let back = (e.altKey ? -1 : 1)
                $.ajax({
                    url: 'ajax/value_shift',
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    data: {
                        "rid": words[0],
                        "param": words[1],
                        "back": back
                    },
                    dataType: 'json',
                    success: function (answer) {
                        $("#"+model+"__"+answer.rid).html(answer.data)
                        me.registerActions()
                    },
                    error: function (answer) {
                        console.error('Error... ' + answer)
                        me.registerActions()
                    },
                })
            }
        })
    }

    registerValuePush() {
        let me = this
        $('#valuepush_ed').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let new_value = $('#ed').val()
            let value = me.zaff_encode(new_value)
            let refs = $("#target_ed").val();
            let words = refs.split("__")
            if (words.includes("bulk")){
                value = me.zaff_encode($("#ed").val())

            }
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
                    $('#roster_' + answer.id).remove()
                    //$div = $('<div>',{id:'roster_'+answer.id,class:"roster"})
                    $('.container').append(answer.new_roster);
                    console.log(answer.new_roster)
                    $('#roster_' + answer.id).removeClass("hidden")
                    $(".for_display_" + answer.id).addClass('hidden');
                    $(".for_edit_" + answer.id).removeClass('hidden');
                    $("#target_ed").val("")
                    $("#ed").val("")
                    me.registerActions()
                    if (me.last_tabbutton != ""){
                        console.log(`${me.last_tabbutton}`)
                        $("#"+me.last_tabbutton).trigger("click")
                    }
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
            let page = $(this).attr("page")
            let target = $(this).attr("target")
            let purpose = $(this).attr("purpose")
            $.ajax({
                url: 'ajax/paginator',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {
                    "page": page,
                    "params": target,
                    "purpose": purpose
                },
                dataType: 'json',
                success: function (answer) {
                    $('.list.'+target).html(answer.html);
                    console.log(answer.html)
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
        $('.list_entry').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let words = miniid.split('__');
            let code = $(this).attr('code');
            let id = words[1];
            $('.list_entry').removeClass('mark');
            $(this).addClass('mark');
            let klass = ""
            if ($(this).hasClass("stregoneria")){
                klass = "stregoneria"
            }
            switch (klass){
                case "stregoneria":
                    console.log("Stregoneria")
                    me.axiomaticPerformers.forEach( (m) => {
                        m.perform(code)
                    });
                    me.registerActions()
                    break
                default:
                    $(".roster").addClass('hidden')
                    $("#roster_" + id).removeClass('hidden')
                    $("#roster_" + id + " .sheet").removeClass('hidden')
                    me.registerActions()
                    break
            }



//             $(".for_display_" + id).removeClass('hidden');
//             $(".for_edit_" + id).addClass('hidden');


        });
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

            //$("#sb_"+id).removeClass('hidden');
            $(".for_display_" + id).removeClass('hidden');
            $(".for_edit_" + id).addClass('hidden');
            console.debug("Showing #roster_" + id + ".sheet")
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
            $(".item").addClass('hidden');
            $(".mini").removeClass('mark');
            $("#mini__" + id).addClass('mark');
            $("#item__" + id).removeClass('hidden');
            $(".for_display_" + id).removeClass('hidden');
            $(".for_edit_" + id).addClass('hidden');
            me.axiomaticPerformers.forEach( (m) => {
                m.perform(code)
            });
            me.registerActions();
        });

        $('.kicker').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let id = $(this).attr('id');
            let code = $(this).attr('param');
            let action = $(this).attr('action');
            let target = $(this).attr('target');
            console.log(id,code,action,target)
            let reds = []
            let blues = []
            if (action == 'run'){
                $(".mate.red").each(function(){
                    reds.push($(this).attr("param"))
                })
                console.log(reds)
                $(".mate.blue").each(function(){
                    blues.push($(this).attr("param"))
                })
                console.log(blues)
            }
            $.ajax({
                url: 'ajax/kicker',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {
                    "id": id,
                    "code": code,
                    "action": action,
                    "target": target,
                    "reds": reds.join(" "),
                    "blues": blues.join(" "),
                },
                dataType: 'json',
                success: function (answer) {
                    if (action == 'view'){
                        $(".container").html("")
                        $(".container").append(answer.html)
                        $(".roster").removeClass("hidden")
                    }
                    if (action == 'select'){
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                    }
                    if (action == 'ini'){
                        if (target == 'combat'){
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                        }
                    }
                    if (action == 'run'){
                        if (target == 'combat'){
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                            $("#svg_area").html(answer.main_html)
                        }
                    }
                    if (action == 'next'){
                        if (target == 'combat'){
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                            $("#svg_area").html(answer.main_html)
                        }
                    }
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ',answer);
                },
            });
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
                console.log("Going to "+link_to)
                window.location = link_to;
            }
        })

        $(".new_spell").off().on('click', function (e) {
            e.preventDefault()
            e.stopPropagation()
            let spell_name = $("#ed").val()
            $.ajax({
                url: 'ajax/new/spell/',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {spell_name:spell_name},
                dataType: 'json',
                success: function (answer) {
                    console.log(answer)
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ')
                    console.error(answer);
                },
            })
        })

    }

    registerShowHide() {
        let me = this;
        $('.showhide').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let tgt = $(this).attr("target");
            console.log("SHOWHIDE")
            if ($(this).hasClass("times")){
                $("."+tgt).addClass("hidden");
                $(".showhide.eye").removeClass("hidden");
                $(".corpus").css("right","0");
                console.log("SHOWHIDE times")
                me.resizeEvent();
            }else if ($(this).hasClass("eye")){
                $("."+tgt).removeClass("hidden");
                $(".showhide.eye").addClass("hidden");
                $(".corpus").css("right","30vw");
                console.log("SHOWHIDE eye")
                me.resizeEvent();
            }else{
                $("."+tgt).toggleClass("hidden");
                if ($("."+tgt).hasClass("hidden")){
                    $(".corpus").css("right","0");
                }else{
                    $(".corpus").css("right","20vw");
                }
                me.resizeEvent();
            }
        });
    }

    resizeEvent(){
        console.log("Chiaroscuro Resize Event")
        let me= this;
        _.forEach(me.globalPerformers,
                (m) => {
                    console.log(m.name," Resize Event")
                    m.resizeEvent();
                }
            );
        _.forEach(me.axiomaticPerformers,
                (m) => {
                    console.log(m.name," Resize Event")
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
        //let url = `ws://192.168.0.25:8083/ws/socket-server/`;
        let host = window.location.hostname
        let protocol = window.location.port
        let url = `ws://${host}:${protocol}/ws/socket-server/`
        console.log(url)
        me.chatSocket = new WebSocket(url)
        me.chatSocket.onmessage = function(e){
            let data = JSON.parse(e.data)
//             console.log("Data:",data)
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
//         console.log("Global Perform");
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
        console.log("Check WS")
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


    fetchExternalSvgResource(file,tgt){
        let me = this;
        d3.xml(file).then(data => {
                d3.select(tgt).node().append(data.documentElement)
            })
//         d3.xml(file, function(error, documentFragment) {
//                 if (error) {
//                     console.log(error);
//                     return;
//                 }
//                 let svgNode = documentFragment
//                     .getElementsByTagName("svg")[0];
//                 me.back.node().appendChild(svgNode);
//                 let innerSVG = me.back.select("svg");
//                 innerSVG.transition().duration(1000).delay(1000)
//                       .select("circle")
//                       .attr("r", 100);
//
//             });
    }

    registerModelForm(){
        let me = this
        $(".model_form_validate").off().on("click", function(e){
            let target = $("#editor").attr("param")
            let target_words = target.split("__")
            console.log(target)

            let model = target_words[0]
            let code = target_words[1]
            let rid = target_words[2]
            console.log(model)
            let json_data={
                model: model,
                code:code,
                rid:rid,
                properties:{}
            }

//             let properties = {}
            $("#editor textarea.modifiable").each(function(e){
                let p = $(this).attr("param")
                let v = $(this).val()
                json_data.properties[p] = v

            })
//             console.log("Properties: ",properties)
//              json_data.properties = properties
             let js = JSON.stringify(json_data)
//             let j = JSON.stringify(json_data)
//             let k = JSON.parse(j)
            console.info(js)
            $.ajax({
                url: 'ajax/overlay/edit/',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {item_info:js},
                 dataType: 'json',
                success: function (answer) {
                    console.log(answer)
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ')
                    console.error(answer);
                },
            })
        })
    }
}