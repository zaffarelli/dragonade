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
        if (config["modules"].includes("carta") == true) {
            let mod = new Carta(this, config);
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
        $('.world').removeClass('shownflex');
        $('.universe').removeClass('hidden');

        $('.world').addClass('hidden');
        $('.universe').addClass('shown');

    }


    registerActions() {
        let me = this;
        me.registerEditables();
        me.registerSheets();
        me.registerLinks();
        me.registerMiniItems();
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
//                     if (params[3] == 'plus'){
//                         change = 'plus';
//                         console.log("Ctrl key")
//
//                     }
//                     else if (e.shiftKey){
//                         change = 'minus'
//                         console.log("Shift key");
//                     }
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
                                $("#ssa_" + answer.id).addClass('hidden');
                                $("#sss_" + answer.id).removeClass('hidden');
                                $("#ssm_" + answer.id).removeClass('hidden');
                                $("#ssg_" + answer.id).removeClass('hidden');
                                $("#ssp_" + answer.id).removeClass('hidden');
                                $("#ssc_" + answer.id).removeClass('hidden');
                                $("#ssd_" + answer.id).removeClass('hidden');
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
            } else {
                console.log("Unknown action...")
            }
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
            me.registerActions();
        });
        $('.skill_switch').off().on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            let miniid = $(this).attr('id');
            let words = miniid.split('_');
            let id = words[0];
            $("#ssa_" + id).toggleClass('hidden');
            $("#sss_" + id).toggleClass('hidden');
            $("#ssm_" + id).toggleClass('hidden');
            $("#ssg_" + id).toggleClass('hidden');
            $("#ssp_" + id).toggleClass('hidden');
            $("#ssc_" + id).toggleClass('hidden');
            $("#ssd_" + id).toggleClass('hidden');
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
            console.log("mini click!")
            $(".item").addClass('hidden');
            $(".mini").removeClass('mark');
            $("#mini__" + id).addClass('mark');
            $("#item__" + id).removeClass('hidden');
            me.axiomaticPerformers.forEach( (m) => m.perform("#item__" + id, code) );

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

    perform() {
        let me = this;
        let no_global = true
        me.prepareAjax();
        me.registerActions();

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
    }

}