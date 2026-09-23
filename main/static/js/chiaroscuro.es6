const ZAFF_MATCHES = [['é', 'WeA_'], ['è', 'WeG_'], ['à', 'WaG_'], ['ï', 'WiT_'], ['ë', 'WeT_'], ['ä', 'WaT_'],
    ['ù', 'WuG_'], ['ç', 'WcC_'], ['ô', 'WoC_'], ['ê', 'WeC_'], ['â', 'WaC_'], [' ', 'Wsp_'], ["'", 'Wsq_'], ['"', 'Wdq_']]

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
        if (config["modules"].includes("appartus") == true) {
            let mod = new Appartus(this, config);
            mod.register();
        }
        if (config["modules"].includes("stregoneria") == true) {
            let mod = new Stregoneria(this, config);
            mod.register();
        }
        if (config["modules"].includes("taccuino") == true) {
            let mod = new Taccuino(this, config);
            mod.register();
        }
        if (config["modules"].includes("combattimento") == true) {
            let mod = new Combattimento(this, config);
            mod.register();
        }
        this.tables = []
        this.last_tabbutton = ""
    }

    prepareWebSocket() {
        let me = this;
        $("#parallax_reveal").off().on('submit', (e) => {
            e.preventDefault();
            let message = e.target.message.value
            me.chatSocket.send(JSON.stringify({
                'type': 'reveal',
                'message': message
            }))
            return false;
        })
        $("#parallax_select").off().on('submit', (e) => {
            e.preventDefault();
            let message = e.target.message.value
            let message_type = e.target.message.value
            me.chatSocket.send(JSON.stringify({
                'type': 'select',
                'message': message
            }))
            return false;
        })
        $("#parallax_random").off().on('submit', (e) => {
            e.preventDefault();

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
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.sheet').addClass('hidden');
    }

    revealUniverse() {
        let me = this;
        $('.world').addClass('shownflex');
        $('.world').removeClass('hidden');
        $('.universe').removeClass('hidden');
    }


    registerActions() {
        let me = this;
        me.prepareAjax()
        me.registerShortcuts()
        me.registerEditor()
        me.registerEditables()
        me.registerStackPull()
        me.registerValuePushEditor()
        // me.registerSheets()
        me.registerLinks()
        me.registerShowHide()
        me.registerShifters()
        me.registerListActions()
    }

    registerShortcuts() {
        let me = this
        $("body").off().on("keyup", (e) => {
            e.preventDefault()
            e.stopPropagation()
            if (e.ctrlKey && e.altKey) {
                switch (e.key) {
                    case "o":
                        $("#options_showhide").trigger('click')
                        break
                }
            }
        })
        $('.closer').off().on('click', function (e) {
            e.preventDefault()
            e.stopPropagation()
            let id = $(this).attr('id')
            let words = id.split('__')
            $("#roster__" + words[0]).remove()
            $("#svg_area").remove()
            me.registerActions()
        })
        $('.tabbutton').off().on('click', function (e) {
            let tgt = $(this).attr("param")
            $(".tabbutton").removeClass("on")
            $("#tabbutton_" + tgt).addClass("on")
            $(".tabpanel").addClass("hidden")
            $("#tabpanel_" + tgt).removeClass("hidden")
            me.last_tabbutton = $(this).attr("id")
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
            let list = $("#ed").val()
            let words = list.split(" ")
            let word = $(this).attr('param')
            if (!words.includes(word)) {
                words.push(word)
            }
            let html = words.join(" ")
            $("#ed").val(html)
        })
    }

    registerListActions() {
        /**
         * From zlist, actions can be done using the option panel... or not
         * @type {Chiaroscuro}
         */
        let me = this
        $('.list_action').off().on('click', function (e) {
            let xxx = $(this).attr('id')
            let words = xxx.split('__')
            let model = words[0]
            let id = words[1]
            let action = words[2]
            let param = words[3]
            let value = words[4]
            console.log(`List action: [${words[0]}:${words[2]}=${words[3]}] required.`)
            switch (action) {
                case "view":
                    me.axiomaticPerformers.forEach((m) => {
                        console.log(`[${m.name}] is ready to handle [${id}]!`)
                        m.handle(id)
                    })
                    me.registerActions()
                    break
                case "edit":
                    me.axiomaticPerformers.forEach((m) => {
                        m.edit(model, id)
                    })
                    me.registerActions()
                    break
                case "randomize":
                    me.axiomaticPerformers.forEach((m) => {
                        m.randomize(model, id)
                    })
                    me.registerActions()
                    break
                case "export":
                    console.log(`Exporting for [${words[0]}] required.`)
                    break
                case "new":
                    $.ajax({
                        url: 'ajax/new',
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        data: {
                            model: model,
                        },
                        dataType: 'json',
                        success: function (answer) {
                            $(".zlist_container").html(answer.data)
                            me.registerActions()
                        },
                        error: function (answer) {
                            console.error('Error... ' + answer);
                        },
                    })
                    break
                case "filter":
                    $.ajax({
                        url: 'ajax/' + words[0].toLowerCase() + '_filter',
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        data: {
                            model: model,
                            param: param,
                            value: value,
                        },
                        dataType: 'json',
                        success: function (answer) {
                            $(".zlist_container").html(answer.data)
                            me.registerActions()
                        },
                        error: function (answer) {
                            console.error('Error... ' + answer);
                        },
                    })
                    break
                default:
                    console.warn(`Unknown list action [${action}] for item [${id}].`)
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
            console.log("Editables")
            if (action == "inc_dec") {
                let params = id.split("__");
                if (params.length > 3) {
                    //if (e.ctrlKey) {
                    change = params[3];
                    //}
                    let data = params[0] + "__" + params[1] + "__" + params[2] + "__" + change;
                    console.log(data)
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
                                $('#roster__' + answer.id).remove()
                                $('#svg_area').append(answer.new_roster);
                                $('#roster__' + answer.id).removeClass("hidden")
                                me.registerActions();
                                if (me.last_tabbutton != "") {
                                    console.log(`${me.last_tabbutton}`)
                                    $("#" + me.last_tabbutton).trigger("click")
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

    registerEditor() {
        let me = this;
        $('.editor').off().on('click', function (e) {
            e.preventDefault()
            e.stopPropagation()
            let id = $(this).attr('id')
            let params = id.split("__")
            if (params.length >= 4) {
                if (params[3] == "value") {
                    if (e.ctrlKey) {
                        let value = $(this).attr("srcval")
                        let encoded_value = me.zaff_decode(value)
                        let data = params[0] + "__" + params[1] + "__" + params[2]
                        // console.log("RegisterEditor")
                        // console.log(data)
                        // console.log(">>>",encoded_value)
                        $("#ed").val(encoded_value)
                        $("#target_ed").val(data)
                        $(this).parent(".interactive_element").addClass("selected")
                        // $("#echo").html(value)
                        me.registerActions()
                    }
                }
            } else {
                console.warn("invalid action...")
            }
        })
    }


    registerShifters() {
        let me = this
        $('.shifter').off().on('click', function (e) {
            e.preventDefault()
            e.stopPropagation()
            let xxx = $(this).attr('id')
            // let model = $(this).attr('model')
            let words = xxx.split('__')
            // console.log(words)
            // console.log(words)
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
                        "model": words[0],
                        "id": words[1],
                        "param": words[2],
                        "back": back
                    },
                    dataType: 'json',
                    success: function (answer) {
                        // console.log(answer.model,answer.id)
                        // console.log(answer.data)
                        $("#" + answer.model.toLowerCase() + "__" + answer.id).html(answer.data)
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

    registerValuePushEditor() {
        let me = this
        $('#valuepush_editor').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let new_value = $('#ed').val()
            let value = me.zaff_encode(new_value)
            let refs = $("#target_ed").val();
            let words = refs.split("__")
            console.log("registerValuePushEditor")
            console.log(words)
            if (words.includes("bulk")) {
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
                    "model": words[0],
                    "id": words[1],
                    "refs": refs
                },
                dataType: 'json',
                success: function (answer) {
                    console.log("Value Push Editor")
                    $('#roster__' + answer.id).remove()
                    $('#svg_area').append(answer.html);
                    $('#roster__' + answer.id).removeClass("hidden")

                    $("#" + answer.model.toLowerCase() + "__" + answer.id).html(answer.data)


                    $("#target_ed").val("")
                    $("#ed").val("")
                    me.registerActions()
                    if (me.last_tabbutton != "") {
                        $("#" + me.last_tabbutton).trigger("click")
                    }
                },
                error: function (answer) {
                    console.error('Error... ' + answer)
                    me.registerActions()
                },
            })
        })
        $("#ed").off().on("click", function (e) {
            if (e.altKey) {
                $("#ed").val("")
                $("#target_ed").val("")
                $("#echo").val("")
            }
        })
    }

    registerMiniItems() {
        let me = this;
        // $('.mini').off().on('click', function (e) {
        //     e.preventDefault();
        //     e.stopPropagation();
        //     let miniid = $(this).attr('id');
        //     let code = $(this).attr('code');
        //     let words = miniid.split('__');
        //     let id = words[1];
        //     $(".item").addClass('hidden');
        //     $(".mini").removeClass('mark');
        //     $("#mini__" + id).addClass('mark');
        //     $("#item__" + id).removeClass('hidden');
        //     $(".for_display_" + id).removeClass('hidden');
        //     $(".for_edit_" + id).addClass('hidden');
        //     me.axiomaticPerformers.forEach((m) => {
        //         m.perform(code)
        //     });
        //     me.registerActions();
        // });

        $('.kicker').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let id = $(this).attr('id');
            let code = $(this).attr('param');
            let action = $(this).attr('action');
            let target = $(this).attr('target');
            console.log(id, code, action, target)
            let reds = []
            let blues = []
            if (action == 'run') {
                $(".mate.red").each(function () {
                    reds.push($(this).attr("param"))
                })
                console.log(reds)
                $(".mate.blue").each(function () {
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
                    if (action == 'view') {
                        $(".container").html("")
                        $(".container").append(answer.html)
                        $(".roster").removeClass("hidden")
                    }
                    if (action == 'select') {
                        $(".middleblock.options").html("")
                        $(".middleblock.options").append(answer.html)
                    }
                    if (action == 'ini') {
                        if (target == 'combat') {
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                        }
                    }
                    if (action == 'run') {
                        if (target == 'combat') {
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                            $("#svg_area").html(answer.main_html)
                        }
                    }
                    if (action == 'next') {
                        if (target == 'combat') {
                            $(".middleblock.options").html("")
                            $(".middleblock.options").append(answer.html)
                            $("#svg_area").html(answer.main_html)
                        }
                    }
                    me.registerActions();
                },
                error: function (answer) {
                    console.error('Error... ', answer);
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
                console.log("Going to " + link_to)
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
                data: {spell_name: spell_name},
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
            if ($(this).hasClass("times")) {
                $("." + tgt).addClass("hidden");
                $(".showhide.eye").removeClass("hidden");
                $(".corpus").css("right", "0");
                console.log("SHOWHIDE times")
                me.resizeEvent();
            } else if ($(this).hasClass("eye")) {
                $("." + tgt).removeClass("hidden");
                $(".showhide.eye").addClass("hidden");
                $(".corpus").css("right", "30vw");
                console.log("SHOWHIDE eye")
                me.resizeEvent();
            } else {
                $("." + tgt).toggleClass("hidden");
                if ($("." + tgt).hasClass("hidden")) {
                    $(".corpus").css("right", "0");
                } else {
                    $(".corpus").css("right", "20vw");
                }
                me.resizeEvent();
            }
        });
    }

    resizeEvent() {
        let me = this;
        _.forEach(me.globalPerformers,
            (m) => {
                m.resizeEvent();
            }
        );
        _.forEach(me.axiomaticPerformers,
            (m) => {
                m.resizeEvent();
            }
        );

    }

    dispatchMessage(type, message) {
        let me = this;
        _.forEach(me.globalPerformers,
            (m) => {
                m.action(type, message);
            }
        );

    }

    zaff_encode(str) {
        let zstr = str
        _.forEach(ZAFF_MATCHES, (m) => {
            zstr = zstr.replaceAll(m[0], m[1])
        })
        return zstr
    }

    zaff_decode(zstr) {
        let str = zstr
        _.forEach(ZAFF_MATCHES, (m) => {
            str = str.replaceAll(m[1], m[0])
        })
        return str
    }

    perform() {
        /* let url = `ws://192.168.0.25:8083/ws/socket-server/`;
        */
        let me = this;
        let no_global = true
        let host = window.location.hostname
        let protocol = window.location.port
        let url = `ws://${host}:${protocol}/ws/socket-server/`
        me.chatSocket = new WebSocket(url)
        me.chatSocket.onmessage = function (e) {
            let data = JSON.parse(e.data)
            if (data.type === "select") {
                $("#info").prepend(
                    `<div>
                    <p>${data.message}</p>
                </div>`
                )
                me.dispatchMessage(data.type, data.message);
            } else {
                me.dispatchMessage(data.type, data.message);
            }
        }
        me.prepareAjax();
        me.registerActions();
        _.forEach(me.globalPerformers,
            (m) => {
                m.perform();
                no_global = false;
            }
        );
        if (no_global) {
            me.revealUI();
        }
        me.prepareWebSocket()
        console.log("Check WS")
    }


}