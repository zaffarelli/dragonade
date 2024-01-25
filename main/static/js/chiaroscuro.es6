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
        this.tables = []
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
    }

    registerEditables() {
        let me = this;
        $('.btn_edit').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let action = $(this).attr('action');
            let id = $(this).attr('id');
            let change = ''
            console.log(action);
            console.log(id);
            if (action == "inc_dec") {
                let params = id.split("__");
                if (params.length > 3) {
                    if (e.ctrlKey) {
                        change = params[3];
                    }
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
                let bvalue = $(this).attr("srcval");
                console.log(bvalue)
                let value = window.atob(bvalue);
                console.log(value)
                if (params.length > 3) {
                    if (e.ctrlKey) {
                        change = params[3];
                    }
                    let data = params[0] + "__" + params[1] + "__" + params[2] + "__" + change;
                    $("#target_ed").val(data);
                    $("#ed").val(value);
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
            let refs = $("#target_ed").val();


            $.ajax({
                url: 'ajax/value_push',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: {
                    "new_value": window.btoa(new_value),
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
                console.log(m.name)
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


    perform() {
        let me = this;
        let no_global = true
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
        //me.resizeEvent();
    }

}