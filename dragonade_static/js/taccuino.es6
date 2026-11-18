class Taccuino extends Modulo {
    constructor(co, config) {
        super(co, config);
        this.name = "Taccuino"
        this.parent = "#svg_area"
        this.fetched = false
    }

    init() {
        super.init()
        let me = this
        me.version = "1.0.0"
        me.supertitle = ""
        me.fontSize = 14
        // Drawing Size
        me.width = me.step * 21.0
        me.height = me.step * 29.7
        me.per_col = 2
        me.per_row = me.per_col
        me.margin = 0.05
        me.header_size = 1
        me.cardw = (21.0 - me.margin*2)/me.per_row
        me.cardh = (29.7 - me.margin*2 - me.header_size)/me.per_col
        me.ox = 0
        me.oy = 0
        // View Size
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        d3.select(me.parent).selectAll("svg").remove();
        me.vis = d3.select(me.parent).append("svg")
            .attr("viewBox", "0 0 " + me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
        me.svg = me.vis.append('g')
            .attr("id", me.code)
            .attr("width", me.width)
            .attr("height", me.height)
            .append("svg:g")
            .attr("id", "print_area")
            .attr("transform", "translate(0,0)")

    }

    drawStregoneria() {
        let me = this;
        let s = {}
        me.klass = "Stregoneria"
        console.log(me.name + " -> Stregoneria")
        me.category = "viaggiatore_spells"
        s = me.datum.payload
        me.filename = s.rid
        console.log(s)
        let ox = 1, oy = 2
        // Statistics
        me.stregoneria = me.back.append("g")
            .attr("class", "stregoneria")
            .attr("id", "stregoneria_" + s.rid)
            .attr("transform", "translate(" + (me.margin)*me.step +"," + (me.margin+me.header_size)*me.step + ")")
        if (s.spells.length == 0) {
            me.stregoneria.append('text')
                .attrs({"x": me.step * (ox + me.margin), "y": (oy + me.margin) * me.step})
                .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "start"})
                .text("Pas de sortilèges pour " + s.name)
        } else {
            let spells = s.spells.split(" ")
            _.forEach(spells, (v, k) => {
                if ((k < me.page*me.per_col*me.per_row)||(k >= (me.page+1)*me.per_col*me.per_row)) return;
                let cardw = 6.85
                let cardh = 9.35
                cardh = me.cardh
                cardw = me.cardw
                let posx = ((k % me.per_row) * cardw)
                let posy = Math.round(((k - 1) / me.per_col)) * cardh
                let incant = me.stregoneria.append('g')
                    .attr("id", `incant_${k}`)
                // .attr('transform',`translate(,${posx*me.step},${posy*me.step})`)
                incant.append('rect')
                    .attr("class", `incantisimo_card`)
                    .attr("id", `card_${k}`)
                    .attrs({
                        "x": posx * me.step,
                        "y": posy * me.step,
                        "rx": me.step * 0.1,
                        "ry": me.step * 0.1,
                        "width": cardw * me.step,
                        "height": cardh * me.step
                    })
                    .style("fill", "#c0c0c0")
                    .style("stroke", "white")
                    .style("stroke-width", "1pt")
                incant.append('rect')
                    .attr("id", `rect_${k}`)
                    .attrs({
                        "x": (posx+me.margin) * me.step,
                        "y": (posy+me.margin) * me.step,
                        "rx": me.step * (me.margin),
                        "ry": me.step * (me.margin),
                        "width": (cardw-(me.margin*2)) * me.step,
                        "height": (cardh-(me.margin*2)) * me.step
                    })
                    .style("fill", "white")
                    .style("stroke", "black")
                    .style("stroke-width", "3pt")
                // Name
                incant.append('text')
                    .attrs({"x": posx * me.step + 0.25 * me.step, "y": posy * me.step + 0.45 * me.step})
                    .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "start"})
                    .text(`${s.spells_details[k].name}`)
                incant.append('text')
                    .attrs({"x": (posx + cardw) * me.step - 0.25 * me.step, "y": posy * me.step + 0.45 * me.step})
                    .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "end"})
                    .text(`${s.spells_details[k].power}`)
                // Basic Metrics
                let delx = 3.25
                let by = 0.15
                let metrics = [
                    {"x": (delx * 0) + 0.1875,"y": 0 + by,"label": "Difficulté","value": s.spells_details[k].difficulty_val},
                    {"x": (delx * 0) + 0.1875,"y": 0.5 + by, "label": "PdR", "value": s.spells_details[k].dps},
                    {"x": (delx * 0) + 0.1875,"y": 1 + by, "label": "Durée", "value": s.spells_details[k].duration_str},
                    {"x": (delx * 1) + 0.1875,"y": 0 + by,"label": "Résistance","value": s.spells_details[k].resistance},
                    {"x": (delx * 1) + 0.1875,"y": 0.5 + by,"label": "Temps Incant.","value": s.spells_details[k].ti_str},
                    {"x": (delx * 1) + 0.1875,"y": 1 + by,"label": "Zone/Taille","value": s.spells_details[k].area_str,},
                    {"x": (delx * 2) + 0.1875,"y": 0 + by, "label": "Portée", "value": s.spells_details[k].range_str},
                    {"x": (delx * 2) + 0.1875,"y": 0.5 + by,"label": "Coût en Songe","value": s.spells_details[k].songe},
                    {"x": (delx * 2) + 0.1875,"y": 1 + by,"label": "Pentacle","value": s.spells_details[k].pentacle_code},
                    {"x": (delx * 0) + 0.1875,"y": 1.5 + by, "label": "Voie", "value": s.spells_details[k].path},
                    {"x": (delx * 1) + 0.1875,"y": 1.5 + by,"label": "Catégorie","value": s.spells_details[k].category},
                    {"x": (delx * 2) + 0.1875,"y": 1.5 + by,"label": "Puissance","value": s.spells_details[k].power},
                ]
                _.forEach(metrics, (e) => {
                    me.drawTinyNumericBlock(incant, e.x + posx, e.y + posy + 1, e.label, e.value)
                })
                // Texts fields
                let stack = 3.25
                let text_metrics = [
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack) * me.step, "label": "Jet", "value": "Rêve + " + s.spells_details[k].roll, "id": `j_${k}`, edit_field: "roll"},
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack) * me.step, "label": "Description", "value": s.spells_details[k].description, "id": `d_${k}`, edit_field: "description"},
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack) * me.step, "label": "Notes", "value": s.spells_details[k].composantes, "id": `n_${k}`, edit_field: "composantes"},
                ]
                let fontratio =0.41
                let fz = me.fontSize * fontratio*2
                let lh = fontratio * me.step
                let ww = (me.cardw-me.margin*15) * me.step
                let lines = 0
                _.forEach(text_metrics, (w)=> {
                    lines = me.appendText(w['label'], w['value'], w['x'], w['y']+ lines * lh, ww, incant, fz)
                })

                // Emplacements des charges
                let basex = 0.25 + posx
                let basey = 13.0 + posy
                let chup = 1.25
                _.forEach([
                    {"code": "tm", "name": "terre", "charge": "ground_charge"},
                    {"code": "sd", "name": "signe", "charge": "hour_charge"},
                    {"code": "cd", "name": "consistance", "charge": "consistency_charge"},
                    {"code": "ed", "name": "emanation", "charge": "emanation_charge"},
                    {"code": "ld", "name": "élément", "charge": "elemental_charge"},
                ], (e, i) => {
                    me.spot_g = incant.append("g")
                        .attr("id", e.code + "_spot_" + s.spells_details[k].rid)
                    me.spot_g.append("circle")
                        .attrs({"cx": (basex + 0.65 + (i * 2.15)) * me.step, "cy": (basey + 0.25) * me.step, "r": 0.65 * me.step})
                        .styles({"fill": "white", "stroke-width": "1pt", "stroke": "black", "stroke-dasharray": "1 3"})
                    if (s.spells_details[k][e.charge]) {
                        d3.select("#" + e.code + "_spot_" + s.spells_details[k].rid).append("image")
                            .attr("class", "relinkable")
                            .attr("xlink:href", "static/main/svg/2026/" + e.code + "_" + s.spells_details[k][e.charge] + ".svg")
                            .attr("width", me.step * 1)
                            .attr("height", me.step * 1)
                            .attr("x", (basex + 0.15 + (i * 2.15)) * me.step)
                            .attr("y", (basey - 0.25) * me.step)
                    }
                })
            })
        }
        // Signature
        me.dragonadeLargeSignature(0.25, 0.25, s.rid, s.name+" - Fiches de Sortilèges")
    }


    drawArtefacts() {
        let me = this;
        let s = {}
        me.klass = "Artefatto"
        console.log(me.name + " -> Artefacts")
        s = me.datum.payload
        me.filename = s.rid
        console.log(s.artefatti_details)
        me.category = "viaggiatore_artefatti"
        let ox = 1, oy = 2
        // Statistics
        me.stregoneria = me.back.append("g")
            .attr("class", "stregoneria")
            .attr("id", "stregoneria_" + s.rid)
            .attr("transform", "translate(" + ox * me.step + "," + oy * me.step + ")")
        me.stregoneria.append('rect')
            .attr("class", "main_rect")
            .attrs({"x": 0, "y": 0, "width": (me.width - me.step * 2), "height": me.height - me.step * 3})
            .style("fill", "white")
            .style("stroke", "black")
            .style("stroke-dasharray", "1 2")
            .style("stroke-width", "1pt")
        if (s.artefatti.length == 0) {
            me.stregoneria.append('text')
                .attrs({"x": me.step * (ox + 0.25), "y": (oy + 0.25) * me.step})
                .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "start"})
                .text("Pas d'Artfacts' pour " + s.name)
        } else {
            let artefatti = s.artefatti.split(" ")
            _.forEach(artefatti, (v, k) => {
                let cardw = 6.35
                let cardh = 8.8
                let posx = ((k % 3) * cardw)
                let posy = Math.round(((k - 1) / 3)) * cardh
                let incant = me.stregoneria.append('g')
                    .attr("id", `incant_${k}`)
                // .attr('transform',`translate(,${posx*me.step},${posy*me.step})`)
                incant.append('rect')
                    .attr("class", `incantisimo_card`)
                    .attr("id", `card_${k}`)
                    .attrs({
                        "x": posx * me.step,
                        "y": posy * me.step,
                        "rx": me.step * 0.1,
                        "ry": me.step * 0.1,
                        "width": cardw * me.step,
                        "height": cardh * me.step
                    })
                    .style("fill", "#c0c0c0")
                    .style("stroke", "white")
                    .style("stroke-width", "5pt")
                incant.append('rect')
                    .attr("id", `rect_${k}`)
                    .attrs({
                        "x": posx * me.step + me.step * 0.1,
                        "y": posy * me.step + me.step * 0.1,
                        "rx": me.step * 0.1,
                        "ry": me.step * 0.1,
                        "width": cardw * me.step - me.step * 0.2,
                        "height": cardh * me.step - me.step * 0.2
                    })
                    .style("fill", "white")
                    .style("stroke", "black")
                    .style("stroke-width", "2pt")
                // Name
                incant.append('text')
                    .attrs({"x": posx * me.step + 0.25 * me.step, "y": posy * me.step + 0.40 * me.step})
                    .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "start"})
                    .text(`${s.artefatti_details[k].name}`)
                incant.append('text')
                    .attrs({"x": (posx + cardw) * me.step - 0.25 * me.step, "y": posy * me.step + 0.40 * me.step})
                    .styles({"font-family": me.titleFont, "font-size": me.fontSize + "pt", "text-anchor": "end"})
                    .text(`${s.artefatti_details[k].power}`)
                // Basic Metrics
                let delx = 2
                let by = -0.25
                let metrics = [
                    {"x": (delx * 0) + 0.1875,"y": 0+by,"label": "Catégorie","value": s.artefatti_details[k].category_str},
                    {"x": (delx * 0) + 0.1875, "y": 0.5+by, "label": "Maîtrise", "value": s.artefatti_details[k].mastery},
                    {"x": (delx * 0) + 0.1875, "y": 1+by, "label": "Période", "value": s.artefatti_details[k].period_str},

                    {"x": (delx * 1) + 0.1875, "y": 0+by, "label": "Points de Rêve", "value": s.artefatti_details[k].pdr},
                    {"x": (delx * 1) + 0.1875, "y": 0.5+by, "label": "Puissance", "value": s.artefatti_details[k].power},
                    {"x": (delx * 1) + 0.1875, "y": 1.0+by, "label": "Prix", "value": s.artefatti_details[k].price}


                ]
                _.forEach(metrics, (e) => {
                    me.drawTinyNumericBlock(incant, e.x + posx, e.y + posy + 1, e.label, e.value)
                })

                // Texts fields
                let stack_y = 2.75
                let lines = 0
                let text_metrics = [
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack_y) * me.step, "label": "Description", "value": s.artefatti_details[k].description},
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack_y) * me.step, "label": "Règles", "value": s.artefatti_details[k].rules},
                    {"x": (posx + 0.35) * me.step, "y": (posy + stack_y) * me.step, "label": "Notes", "value": s.artefatti_details[k].notes},
                ]
                _.forEach(text_metrics, (w) => {
                    lines = me.appendText(w['label'], w['value'], w['x'], w['y'] + (lines) * (0.24 * me.step), 5.75 * me.step, incant, me.fontSize * 0.63)
                })

                // lines = me.appendText("Règles", s.artefatti_details[k].rules,(posx+0.35)*me.step,(posy+stack)*me.step+lines*lh,ww,incant,fz)
                // lines = me.appendText("Notes", s.artefatti_details[k].notes,(posx+0.35)*me.step,(posy+stack)*me.step+lines*lh,ww,incant,fz)
                // // Emplacements des charges
                // let basex = 0.125 + posx
                // let basey = 7.8 + posy
                // let chup = 1.25
                // _.forEach([
                //     {"code": "tm", "name": "terre", "charge": "ground_charge"},
                //     {"code": "sd", "name": "signe", "charge": "hour_charge"},
                //     {"code": "cd", "name": "consistance", "charge": "consistency_charge"},
                //     {"code": "ed", "name": "emanation", "charge": "emanation_charge"},
                //     {"code": "ld", "name": "élément", "charge": "elemental_charge"},
                // ], (e, i) => {
                //     me.spot_g = incant.append("g")
                //         .attr("id", e.code + "_spot_" + s.spells_details[k].rid)
                //     me.spot_g.append("circle")
                //         .attrs({"cx": (basex + 0.55 + (i * 1.25)) * me.step, "cy": (basey + 0.25) * me.step, "r": 0.5 * me.step})
                //         .styles({"fill": "white", "stroke-width": "1pt", "stroke": "black", "stroke-dasharray": "1 3"})
                //     // me.spot_g.append("text")
                //     //     .attrs({"x":(basex+1+(i*2.5))*me.step,"y":(basey+2.5)*me.step})
                //     //     .styles({"fill":"black","stroke":"black", "stroke-width":"0.5pt", "text-anchor":"middle", "font-family":me.baseFont, "font-size":"8pt"})
                //     //     .text(e.name.toUpperCase())
                //     if (s.spells_details[k][e.charge]) {
                //         d3.select("#" + e.code + "_spot_" + s.spells_details[k].rid).append("image")
                //             .attr("class", "relinkable")
                //             .attr("xlink:href", "static/main/svg/2026/" + e.code + "_" + s.spells_details[k][e.charge] + ".svg")
                //             .attr("width", me.step * 1)
                //             .attr("height", me.step * 1)
                //             .attr("x", (basex + 0.05 + (i * 1.25)) * me.step)
                //             .attr("y", (basey - 0.25) * me.step)
                //     }
                // })

            })


        }
        // Signature
        me.dragonadeSignature(1, 1, s.rid, "Fiche d'Artefacts Draconiques de " + s.name)
    }


    // showbb(tgt,k) {
    //     let me = this
    //     let item = d3.select(tgt+"_rect")
    //     let bb = item.node().getBoundingClientRect()
    //     item.append("rect")
    //         .attr("class", "bb")
    //         .attrs({"x": 0, "y": 0, "width": bb.width, "height": bb.height})
    //         .styles({"fill": "#a020202f", "stroke": "#a02020", "stroke-width": "1pt"})
    // }


    edit(model, id) {
        let data = super.edit(model, id)
        let me = this
        console.log(`[${me.name}] is ready to edit [${model}::${id}] !`)
        $.ajax({
            url: 'ajax/edit',
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {
                "id": id,
                "model": model,
            },
            dataType: 'json',
            success: function (answer) {
                me.datum = {}
                me.datum['id'] = answer['id']
                me.datum['type'] = answer['type']
                me.datum['payload'] = answer['payload']
                $("<div id='svg_area'></div>").insertBefore('.zlist_container')
                // console.log(answer.html)
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

    randomize(model, id) {
        let data = super.edit(model, id)
        let me = this
        console.log(`[${me.name}] is ready to edit [${model}::${id}] !`)
        $.ajax({
            url: 'ajax/randomize',
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data: {
                "id": id,
                "model": model,
            },
            dataType: 'json',
            success: function (answer) {
                me.datum = {}
                me.datum['id'] = answer['id']
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

    postFetch() {
        super.postFetch()
        let me = this
        me.fetched = true
        switch (me.fileprefix) {
            case "spells":
                me.prepareSpells()
                me.drawBack()
                me.drawStregoneria()
                break;
            case "artefatti":
                me.drawBack()
                me.drawArtefacts()
                break;
            default:
                console.log("Nothing to do")
                break

        }
        me.zoomActivate()
    }

    goBack() {
        super.goBack()
        $("#svg_area").remove()
    }

    prepareSpells(){
        let me = this
        let spells = me.datum.payload.spells.split(" ")
        me.pages_count = Math.ceil(spells.length / (me.per_row*me.per_col))
    }

    handleSpells(code) {
        super.handleSpells()
        let me = this
        me.code = code
        me.page = 0
        me.fileprefix = "spells"
        me.filename = me.code
        $("<div id='svg_area'></div>").insertBefore('.zlist_container')
        me.init()
        me.fetch("viaggiatore", code)

    }

    handleArtefacts(code) {
        super.handleArtefacts()
        let me = this
        me.code = code
        me.page = 0
        me.fileprefix = "artefatti"
        me.filename = me.code
        $("<div id='svg_area'></div>").insertBefore('.zlist_container')
        me.init()
        me.fetch("viaggiatore", code)
        let artefatti = me.datum.payload.artefatti.split(" ")
        me.pages_count = Math.ceil(artefatti.length / (me.per_row*me.per_col))
    }


}