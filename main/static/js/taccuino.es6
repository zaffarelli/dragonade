class Taccuino extends Modulo {
    constructor(co, config) {
        super(co, config);
        this.name = "Taccuino"
        this.parent = "#svg_area"
        this.fetched = false
    }

    init() {
        super.init();
        let me = this;
    }

    edit(model,rid){
        let data = super.edit(model,rid)
        let me = this
        console.log(`[${me.name}] is ready to edit [${model}::${rid}] !`)
        $.ajax({
            url: 'ajax/edit',
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {
                "rid": rid,
                "model": model,
            },
            dataType: 'json',
            success: function (answer) {
                me.datum = {}
                me.datum['rid'] = answer['rid']
                me.datum['type'] = answer['type']
                me.datum['payload'] = answer['payload']
                $("<div id='svg_area'></div>").insertBefore('.zlist_container')
                console.log(answer.html)
                $('#svg_area').html(answer.html)
                $('.roster').removeClass("hidden")
                me.postEdit()
                me.co.registerActions()
            },
            error: function (answer) {
                console.error('Error... ' + answer)
                me.co.registerActions()
            },
        })
        return data
    }

}